from datetime import datetime
import logging
import math

from scipy.integrate import ode
from serial import Serial
from serial.tools import list_ports
from matplotlib import pyplot as plt


class Spring:
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG, filename="spring.log", filemode="w")
        available_ports = list(list_ports.grep('/dev/ttyACM', include_links=True))
        if not available_ports:
            raise ValueError("no available ports")
        logging.info("available ports {}, choose port {}"
                     .format([port.device for port in available_ports], available_ports[0].device))
        self.ser = Serial(available_ports[0].device, baudrate=115200)

        self.x = 0
        self.velocity = 0

        self.mass = 0.003
        # self.damping = None
        self.k = None
        self.rate = None
        self.k1 = None
        self.k2 = None
        self.k3 = None
        self.left_point = None
        self.right_point = None
        self.drop_point = None
        self.cycle = None
        self.profile = None

        self.estimated_delta_time = 0.0037
        self.last_time = None

        self.xs = []
        self.x_times = []

        self.proximities = []
        self.proximity_times = []

        self.forces = []
        self.force_times = []

        self.buffer = bytearray()



        def f(t, y, force, k, damping):
            displacement, velocity = y
            return [velocity,
                    (force - k * displacement - damping * velocity) / self.mass]

        self.ode_solver = ode(f)
        self.ode_solver.set_integrator("dopri5")
        self.ode_solver.set_initial_value([0, 0], 0)

    def _set_parameters(self, profile, k1=None, k2=None, k3=None,
                        left_point=None, right_point=None, drop_point=None, cycle=None):
        self.profile = profile
        self.ode_solver.set_initial_value([0, 0], 0)
        self.x = 0

        if profile == "constant":
            self.k = k1
        elif profile == 'linear':
            self.left_point = left_point / 1000
            self.right_point = right_point / 1000
            distance = self.right_point - self.left_point
            self.rate = (k2 - k1) / distance
            self.k1 = k1
            self.k2 = k2
        elif profile == 'click':
            self.k1 = k1
            self.k2 = k2
            self.left_point = left_point / 1000
            self.right_point = right_point / 1000
        elif profile == "pseudo_click":
            self.k1 = k1
            self.k2 = k2
            self.k3 = k3
            self.left_point = left_point / 1000
            self.right_point = right_point / 1000
        elif profile == 'drop':
            self.k1 = k1
            self.k2 = k2
            self.drop_point = drop_point / 1000

    def _get_k(self):
        k = None
        if self.profile == 'constant':
            k = self.k
        elif self.profile == 'linear':
            if self.x <= self.left_point:
                k = self.k1
            elif self.x < self.right_point:
                k = self.rate * (self.x - self.left_point) + self.k1
            else:
                k = self.k2
        elif self.profile == 'click':
            if self.left_point < self.x < self.right_point:
                k = self.k2
            else:
                k = self.k1
        elif self.profile == "pseudo_click":
            if self.x < self.left_point:
                k = self.k1
            elif self.x < self.right_point:
                k = self.k2
            else:
                k = self.k3
        elif self.profile == 'drop':
            if self.x < self.drop_point:
                k = self.k1
            else:
                k = self.k2
        damping = 2 * math.sqrt(self.mass * k)
        return k, damping

    def set_profile(self, profile):
        if profile == "low":
            self._set_parameters("constant", k1=5)
        elif profile == "high":
            self._set_parameters("constant", k1=35)
        elif profile == "medium":
            self._set_parameters("constant", k1=20)
        elif profile == "increasing":
            self._set_parameters("linear", k1=5, k2=40, left_point=0, right_point=100)
        elif profile == "decreasing":
            self._set_parameters("linear", k1=40, k2=10, left_point=0, right_point=100)
        elif profile == "click":
            self._set_parameters("click", k1=5, k2=35, left_point=50, right_point=60)
        elif profile == "drop":
            self._set_parameters("drop", k1=30, k2=10, drop_point=60)
        elif profile == "pseudo_click":
            self._set_parameters("pseudo_click", k1=5, k2=35, k3=20, left_point=50, right_point=60)
        else:
            raise ValueError("unknown profile name '{}'".format(profile))

    def run(self):
        while True:
            num = self.ser.in_waiting
            if num > 0:
                data = self.ser.read(1)
                now = datetime.now()
                if data == b'\n':
                    logging.info("at {}, from serial get {}"
                                 .format(now, self.buffer))
                    try:
                        buffer_data = self.buffer.decode()
                        key, value = buffer_data.split(maxsplit=1)
                        if key == 'f':
                            force_sensor, setpoint, proximity, output = value.split()
                            force_sensor, setpoint = int(force_sensor), float(setpoint)
                            if self.last_time:
                                delta_time = now.timestamp() - self.last_time
                                self.estimated_delta_time = 0.8 * self.estimated_delta_time + 0.2 * delta_time
                            force = math.exp(7.15) * (force_sensor ** 1.32) * 9.8 / (
                                    1000 * (10240 - 10 * force_sensor) ** 1.32)

                            k, damping = self._get_k()
                            logging.info("sensor: {} force: {} output: {}, k: {}"
                                         .format(force_sensor, force, self.x * 1000, k))
                            self._apply_f(force, k, damping)
                            self._send_x()
                            self.last_time = now.timestamp()
                            proximity, output = float(proximity), float(output)
                            self.proximity_times.append(now.timestamp())
                            self.proximities.append(proximity)
                            self.force_times.append(now.timestamp())
                            self.forces.append(force)

                    except UnicodeDecodeError:
                        pass
                    except ValueError as e:
                        logging.debug(e)
                        logging.debug(self.buffer)
                    finally:
                        self.buffer = bytearray()
                else:
                    self.buffer.extend(data)

    def _apply_f(self, force, k, damping):
        self.ode_solver.set_f_params(force, k, damping)
        next_t = self.ode_solver.t + self.estimated_delta_time
        y = self.ode_solver.integrate(next_t)
        if self.ode_solver.successful():
            x, v = y
            if x > 140 / 1000:
                x = 140 / 1000
                v = 0
                self.ode_solver.set_initial_value([x, v], next_t)
            self.x = x
        else:
            raise ValueError("not successful")

    def _send_x(self):
        x = self.x * 1000
        now = datetime.now()
        self.xs.append(x)
        self.x_times.append(now.timestamp())
        self.ser.write((str(int(x)) + "s").encode())
        logging.info("at {}, send x {}".format(now, int(x)))

    def terminate(self):
        fig, ax = plt.subplots()
        ax.plot(self.proximity_times, self.proximities, 'b-')
        ax.plot(self.x_times, self.xs, 'g-.')
        ax.plot(self.force_times, self.forces, 'y--')
        plt.savefig('800.svg')
        delta_times = [a - b for a, b in zip(self.x_times[1:], self.x_times[:-1])]
        logging.info("average delta_time {}".format(sum(delta_times) / len(delta_times)))


def main():
    spring = Spring()
    try:
        # spring.set_profile("low")
        # spring.set_profile("high")
        # spring.set_profile("medium")
        # spring.set_profile("increasing")
        # spring.set_profile("decreasing")
        # spring.set_profile("click")
        # spring.set_profile("drop")
        spring.set_profile("pseudo_click")
        spring.run()
    except KeyboardInterrupt:
        spring.terminate()


if __name__ == '__main__':
    main()
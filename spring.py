import threading
import logging
import math
import time

from scipy.integrate import ode
from serial import Serial
from serial.tools import list_ports
import csv


class Spring(threading.Thread):
    def __init__(self, callback=None):
        threading.Thread.__init__(self)
        logging.basicConfig(level=logging.DEBUG, filename="spring.log", filemode="w")
        available_ports = list(list_ports.grep('/dev/tty', include_links=True))
        if not available_ports:
            raise ValueError("no available ports")
        logging.info("available ports {}, choose port {}"
                     .format([port.device for port in available_ports], available_ports[0].device))
        self.ser = Serial(available_ports[0].device, baudrate=115200)

        self.callback = callback

        self.x = 0
        self.prev_x = 0
        self.velocity = 0

        self.mass = 0.0001
        self.k = None
        self.rate = None
        self.down_rate = None
        self.k1 = None
        self.k2 = None
        self.k3 = None
        self.left_point = None
        self.middle_point = None
        self.right_point = None
        self.step_point = None
        self.profile = None
        self.width = None
        self.position = None

        self.force_sensor_storage = []
        self.average_force = None

        self.estimated_delta_time = 0.0037
        self.last_time = None

        self.buffer = bytearray()

        self.x_lock = threading.Lock()
        self.terminate_event = threading.Event()

        self.csvfile = open("log.csv", "wb")
        self.writer = csv.writer(self.csvfile)

        def f(t, y, force, k, damping):
            displacement, velocity = y
            return [velocity,
                    float(force - k * displacement - damping * velocity) / self.mass]

        self.ode_solver = ode(f)
        self.ode_solver.set_integrator("dopri5")
        self.ode_solver.set_initial_value([0, 0], 0)

    def run(self):
        while not self.terminate_event.is_set():
            num = self.ser.in_waiting
            if num > 0:
                data = self.ser.read(1)
                now = time.time()
                if data == b'\n':
                    logging.info("at %s, from serial get %s", now, self.buffer)
                    try:
                        buffer_data = self.buffer.decode()
                        key, value = buffer_data.split(" ", 1)
                        if key == 'f':
                            # logging.info("f send at %s", self.f_received_time)
                            force_sensor, setpoint, proximity, output = value.split()
                            force_sensor, proximity = int(force_sensor), float(proximity)
                            setpoint, output = float(setpoint), float(output)
                            if self.callback:
                                self.callback("%0.3f" % setpoint)
                            if self.last_time:
                                delta_time = now - self.last_time
                                self.estimated_delta_time = 0.8 * self.estimated_delta_time + 0.2 * delta_time
                            # force = math.exp(7.15) * (force_sensor ** 1.32) * 9.8 / (
                            #         1000 * (10240 - 10 * force_sensor) ** 1.32)
                            force = 9.7 * force_sensor / (1024 - force_sensor)
                            if self.average_force:
                                self.average_force = 0.95 * self.average_force + 0.05 * force
                            else:
                                self.average_force = force
                            logging.info("sensor: %d force: %0.2f average: %0.2f"
                                         , force_sensor, force, self.average_force)
                            if self.profile != "fixed":
                                x_to_k = int(round(self.x * 1000))
                                k, damping = self._get_k(x_to_k)
                                self._apply_f(self.average_force, k, damping)
                                x = int(round(self.x * 1000))
                                logging.info("x = %s", x)
                                self.writer.writerow([now, self.average_force, x_to_k, x, setpoint, proximity, k, output])
                                if x != self.prev_x:
                                    self.ser.write((str(x) + "s").encode())
                                    logging.info("at %s, send x %d", now, x)
                                    self.prev_x = x
                            else:
                                x = self.position
                                self.ser.write((str(x) + "s").encode())
                                logging.info("at %s, send x %d", now, x)
                            self.last_time = now
                    except UnicodeDecodeError:
                        pass
                    except ValueError as e:
                        logging.debug(e)
                        logging.debug(self.buffer)
                    finally:
                        self.buffer = bytearray()
                else:
                    self.buffer.extend(data)

    def _set_parameters(self, profile, k1=None, k2=None, k3=None,
                        left_point=None, right_point=None, step_point=None,
                        width=None, position=None):
        self.profile = profile
        self.ode_solver.set_initial_value([0, 0], 0)
        self.x = 0

        if profile == "constant":
            self.k = k1
        elif profile == 'fixed':
            self.position = position
        elif profile == 'linear':
            self.left_point = left_point
            self.right_point = right_point
            self.rate = float(k2 - k1) / (right_point - left_point)
            self.k1 = k1
            self.k2 = k2
        elif profile == "pseudo_click":
            self.k1 = k1
            self.k2 = k2
            self.k3 = k3
            self.left_point = left_point
            self.right_point = right_point
            self.middle_point = float(self.left_point + self.right_point) / 2
            self.width = width
            self.rate = float(k2 - k1) / (self.middle_point - width - self.left_point)
            self.down_rate = float(k3 - k2) / (self.right_point - (self.middle_point + width))
        elif profile == 'step':
            self.k1 = k1
            self.k2 = k2
            self.step_point = step_point

    def _get_k(self, x):
        k = None
        if self.profile == 'constant':
            k = self.k
        elif self.profile == 'linear':
            if x < self.left_point:
                k = self.k1
            elif x < self.right_point:
                k = self.rate * (x - self.left_point) + self.k1
            else:
                k = self.k2
        elif self.profile == "pseudo_click":
            if x < self.left_point:
                k = self.k1
            elif x < self.middle_point - self.width:
                k = self.rate * (x - self.left_point) + self.k1
            elif x < self.middle_point + self.width:
                k = self.k2
            elif x < self.right_point:
                k = self.down_rate * (x - (self.middle_point + self.width)) + self.k2
            else:
                k = self.k3
        elif self.profile == 'step':
            if x < self.step_point:
                k = self.k1
            else:
                k = self.k2
        damping = 2 * math.sqrt(self.mass * k)
        logging.info("x = %s, k = %s, damping = %0.3f", x, k, damping)
        return k, damping

    def set_profile(self, profile, length="long"):
        self.profile = profile
        if profile == "low":
            self._set_parameters("constant", k1=3)
        elif profile == "medium":
            if length == "short":
                self._set_parameters("constant", k1=25)
            else:
                self._set_parameters("constant", k1=25)
        elif profile == "empty":
            self._set_parameters("fixed", position=70)
        elif profile == "high":
            self._set_parameters("fixed", position=0)
        elif profile == "increasing":
            if length == "long" or length == "middle":
                self._set_parameters("step", k1=5, k2=50, step_point=15)
            elif length == "short":
                self._set_parameters("step", k1=5, k2=50, step_point=15)
        elif profile == "decreasing":
            if length == "long":
                self._set_parameters("linear", k1=50, k2=13, left_point=0, right_point=60)
            elif length == "middle":
                self._set_parameters("linear", k1=50, k2=13, left_point=0, right_point=30)
            elif length == "short":
                self._set_parameters("linear", k1=50, k2=20, left_point=0, right_point=15)
        elif profile == "click":
            if length == "long":
                self._set_parameters("pseudo_click", k1=5, k2=30, k3=5, left_point=30, right_point=50, width=5)
            elif length == "middle":
                self._set_parameters("pseudo_click", k1=5, k2=30, k3=5, left_point=20, right_point=40, width=5)

            elif length == "short":
                self._set_parameters("pseudo_click", k1=5, k2=30, k3=5, left_point=10, right_point=20, width=2)
        elif profile == "drop":
            if length != "short":
                self._set_parameters("step", k1=150, k2=3, step_point=10)
            else:
                self._set_parameters("step", k1=200, k2=3, step_point=5)

        else:
            raise ValueError("unknown profile name '{}'".format(profile))

    def _apply_f(self, force, k, damping):
        self.ode_solver.set_f_params(force, k, damping)
        next_t = self.ode_solver.t + self.estimated_delta_time
        y = self.ode_solver.integrate(next_t)
        if self.ode_solver.successful():
            x, v = y
            with self.x_lock:
                self.x = x
        else:
            raise ValueError("not successful")

    def terminate(self):
        self.terminate_event.set()
        self.csvfile.close()


def main():
    spring = Spring()
    spring.set_profile("low", "short")
    # spring.set_profile("high", "short")
    # spring.set_profile("medium", "short")
    # spring.set_profile("increasing", "short")
    # spring.set_profile("decreasing", "short")
    # spring.set_profile("click", "short")
    # spring.set_profile("drop", "short")
    # spring.set_profile("empty")
    spring.start()
    try:
        while spring.is_alive:
            spring.join(1)
    except KeyboardInterrupt:
        spring.terminate()


if __name__ == '__main__':
    main()

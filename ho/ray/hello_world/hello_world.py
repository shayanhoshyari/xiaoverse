from ray import serve
from ray.serve.handle import DeploymentHandle
import time


@serve.deployment
class MyFirstDeployment:
    # Take the message to return as an argument to the constructor.
    def __init__(self, msg):
        self.msg = msg

    def __call__(self):
        return self.msg


def main():
    my_first_deployment = MyFirstDeployment.bind("Hello world!")
    handle: DeploymentHandle = serve.run(my_first_deployment)
    assert handle.remote().result() == "Hello world!"
    time.sleep(100)


if __name__ == "__main__":
    main()

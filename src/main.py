import hello_pb2
import hello_pb2_grpc
from concurrent import futures
import logging
import grpc
from grpc_reflection.v1alpha import reflection


class Greeter(hello_pb2_grpc.GreeterServicer):
    # pyrefly: ignore [bad-override]
    def SayHello(self, request, context):
        print(f"Received request: {request.name}")
        return hello_pb2.HelloReply(message=f"Hello, {request.name}!")

    # pyrefly: ignore [bad-override]
    def SayHelloAgain(self, request, context):
        return hello_pb2.HelloReply(message=f"Hello again, {request.name}!")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    hello_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)

    SERVICE_NAMES = (
    hello_pb2.DESCRIPTOR.services_by_name['Greeter'].full_name,
    reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    
    server.add_insecure_port("[::]:50051")

    print("Server started on port 50051")
    server.start()

    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()

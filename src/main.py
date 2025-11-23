import hello_pb2
import hello_pb2_grpc
from concurrent import futures
import logging
import grpc


# 1. Create a class that inherits from the generated Servicer
class Greeter(hello_pb2_grpc.GreeterServicer):
    # Implement the SayHello method defined in the proto
    def SayHello(self, request, context):
        # 'request' is the HelloRequest object
        # 'context' contains RPC-specific metadata (timeouts, metadata, etc.)
        print(f"Received request: {request.name}")
        return hello_pb2.HelloReply(message=f"Hello, {request.name}!")

    # Implement the SayHelloAgain method
    def SayHelloAgain(self, request, context):
        return hello_pb2.HelloReply(message=f"Hello again, {request.name}!")


def serve():
    # 2. Create the gRPC server
    # You must provide a thread pool for processing requests
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # 3. Register your class with the server
    hello_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)

    # 4. Bind the port
    # [::] listens on all IPv4 and IPv6 interfaces
    server.add_insecure_port("[::]:50051")

    print("Server started on port 50051")
    server.start()

    # Keep the thread alive
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()

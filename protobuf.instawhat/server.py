#!/usr/bin/python3
import sys
import socket
import instawhat_pb2 as instawhat

SOCKET_PORT = int(sys.argv[1])


class User:
    def __init__(self, user_id, user_password):
        self.id = user_id
        self.password = user_password
        self.photos = []

class Server:
    def __init__(self):
        self.users = {
            'John.Doe': User('John.Doe', 'password'),
            'Jane.Doe': User('Jane.Doe', 'password')
        }

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('', SOCKET_PORT))
        print(f'Server listening on port {SOCKET_PORT}')

    def run(self):
        while True:
            data, client = self.sock.recvfrom(4096)
            request = instawhat.Request()
            request.ParseFromString(data)
            print(f'Request received from {client}')

            operation = self.get_operation_handler(request)

            if operation:
                response = operation(request)
            else:
                response = instawhat.Response()
                response.error.code = instawhat.Error.INVALID_DATA
                response.error.message = 'Invalid operation'

            self.sock.sendto(response.SerializeToString(), client)

    def get_operation_handler(self, request):
        operation_type = request.WhichOneof('request')
        return getattr(self, operation_type.lower(), None)

    def post_photo(self, request):
        user = self.users[request.post_photo.credentials[0]]
        response = instawhat.Response()

        if not user:
            response.error.code = instawhat.Error.NOT_FOUND
            response.error.message = 'User not found'
            return response

        if user.password != request.post_photo.credentials[1]:
            response.error.code = instawhat.Error.UNAUTHORIZED
            response.error.message = 'Invalid password'
            return response

        if request.post_photo.photo_url in user.photos:
            response.error.code = instawhat.Error.ALREADY_EXISTS
            response.error.message = 'Photo already posted'
            return response

        user.photos.append(request.post_photo.photo_url)
        response.success.message = 'Photo posted'
        print(f'Post photo {request.post_photo.photo_url}')
        return response

    # No functionality implemented
    def comment_photo(self, request):
        print(f'Comment photo {request.comment_photo.photo_url}:')
        print(f'"{request.comment_photo.comment}"')
        response = instawhat.Response()
        response.success.message = 'Photo commented'
        return response

    # No functionality implemented
    def rate_photo(self, request):
        print(f'Rate photo {request.rate_photo.photo_url}: '
            + f'{request.rate_photo.rating}')

        response = instawhat.Response()
        response.success.message = 'Photo rated'
        return response

    # No functionality implemented
    def like_photo(self, request):
        print(f'Like photo {request.like_photo.photo_url}')
        response = instawhat.Response()
        response.success.message = 'Photo liked'
        return response

    # No functionality implemented
    def delete_photo(self, request):
        print(f'Delete photo {request.delete_photo.photo_url}')
        response = instawhat.Response()
        response.success.message = 'Photo deleted'
        return response

    # No functionality implemented
    def get_last_photos(self, request):
        print(f'Get photos of user {request.get_last_photos.user_id}')
        response = instawhat.GetLastPhotosResponse()
        response.photo_urls.extend(['photo1', 'photo2', 'photo3'])
        response.success.message = 'Photos retrieved'
        return response


if __name__ == '__main__':
    server = Server()
    server.run()

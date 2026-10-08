#!/usr/bin/python3

import sys

import socket
import argparse

import instawhat_pb2 as instawhat

CREDENTIALS = ['John.Doe', 'password']


class InstaWhatClient:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = (host, port)

    def handle_request(self, request, ResponseType=instawhat.Response):
        self.sock.sendto(
            request.SerializeToString(),
            self.server_address
        )

        data = self.sock.recv(4096)
        response = ResponseType()
        response.ParseFromString(data)

        self.sock.close()
        return response

    def post_photo(self, **kwargs):
        request = instawhat.Request()
        request.post_photo.credentials.extend(CREDENTIALS)
        request.post_photo.photo_url = kwargs['photo_url']
        return self.handle_request(request)

    def comment_photo(self, **kwargs):
        request = instawhat.Request()
        request.comment_photo.credentials.extend(CREDENTIALS)
        request.comment_photo.owner_id = kwargs['owner_id']
        request.comment_photo.photo_url = kwargs['photo_url']
        request.comment_photo.comment = kwargs['comment']
        return self.handle_request(request)

    def rate_photo(self, **kwargs):
        request = instawhat.Request()
        request.rate_photo.credentials.extend(CREDENTIALS)
        request.rate_photo.owner_id = kwargs['owner_id']
        request.rate_photo.photo_url = kwargs['photo_url']
        request.rate_photo.rating = kwargs['rating']
        return self.handle_request(request)

    def like_photo(self, **kwargs):
        request = instawhat.Request()
        request.like_photo.credentials.extend(CREDENTIALS)
        request.like_photo.photo_url = kwargs['photo_url']
        request.like_photo.owner_id = kwargs['owner_id']
        return self.handle_request(request)

    def delete_photo(self, **kwargs):
        request = instawhat.Request()
        request.delete_photo.credentials.extend(CREDENTIALS)
        request.delete_photo.photo_url = kwargs['photo_url']
        return self.handle_request(request)

    def get_last_photos(self, **kwargs):
        request = instawhat.Request()
        request.get_last_photos.user_id = kwargs['user_id']

        return self.handle_request(
            request, instawhat.GetLastPhotosResponse
        )


def main():
    client = InstaWhatClient(args.host, args.port)
    response = getattr(client, args.operation)(**vars(args))

    if response.HasField('error'):
        print('Error '
            + f'{instawhat.Error.ErrorCode.Name(response.error.code)}'
            + ': ' + response.error.message)
        sys.exit(1)

    print('Success: ' + response.success.message)
    if args.operation == 'get_last_photos':
        for photo_url in response.photo_urls:
            print(photo_url)


parser = argparse.ArgumentParser(description="Client for InstaWhat")

parser.add_argument("host", help="Host address of the server")
parser.add_argument("port", type=int, help="Port number of the server")
subparsers = parser.add_subparsers(dest="operation", help="Available operations")

post_photo_parser = subparsers.add_parser("post_photo", help="Post a photo")
post_photo_parser.add_argument("photo_url", help="URL of the photo")

comment_photo_parser = subparsers.add_parser("comment_photo", help="Comment on a photo")
comment_photo_parser.add_argument("owner_id", help="Owner ID of the photo")
comment_photo_parser.add_argument("photo_url", help="URL of the photo")
comment_photo_parser.add_argument("comment", help="Comment to be added")

rate_photo_parser = subparsers.add_parser("rate_photo", help="Rate a photo")
rate_photo_parser.add_argument("owner_id", help="Owner ID of the photo")
rate_photo_parser.add_argument("photo_url", help="URL of the photo")
rate_photo_parser.add_argument("rating", type=int, help="Rating to be given")

like_photo_parser = subparsers.add_parser("like_photo", help="Like a photo")
like_photo_parser.add_argument("owner_id", help="Owner ID of the photo")
like_photo_parser.add_argument("photo_url", help="URL of the photo")

delete_photo_parser = subparsers.add_parser("delete_photo", help="Delete a photo")
delete_photo_parser.add_argument("photo_url", help="URL of the photo")

get_last_photos_parser = subparsers.add_parser("get_last_photos", help="Get last 20 photos of a user")
get_last_photos_parser.add_argument("user_id", help="User ID whose photos to retrieve")

args = parser.parse_args()

main()

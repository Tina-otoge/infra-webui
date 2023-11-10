import bcrypt

from . import config


def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


def check_token(token):
    for saved_token in config.secrets.get("tokens", []):
        saved_token = str(saved_token)
        if saved_token[0] == "$":
            if check_password(token, saved_token):
                return True
        else:
            if token == saved_token:
                return True
    return False


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("password")
    args = parser.parse_args()
    print(hash_password(args.password))

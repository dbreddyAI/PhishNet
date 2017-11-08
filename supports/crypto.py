from hashlib import sha256

salt = 'Dxi$iPgeGfWLi3ZV2B5$6qQ#Ce$h4AEhi^#dLNLQn28FYVZyXpK3ma!27dHQzsYH5IN*C21!BFFmP7@KZ8VHdeqeAuZehnw^XLyi'


def make_hash(string):
    return sha256((string + salt).encode()).hexdigest()

def verify(pas, pass_hash):
    return make_hash(pas) == pass_hash

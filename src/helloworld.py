import fire

def hello(name="World"):
    return "Hello %s, Nice to meet you." % name

if __name__ == "__main__":
    fire.Fire(hello)
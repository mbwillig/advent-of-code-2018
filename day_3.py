def day3a():
    import numpy as np

    cloth = np.zeros([1000, 1000])

    with open("day_3_AOC") as fh:
        data = fh.readlines()

    for request in data:
        requestnr, _, offsets, size = request.strip().split(" ")
        requestnr = int(requestnr.strip("#"))
        left_offset, upper_offset = [int(x) for x in offsets.strip(":").split(",")]
        width, height = [int(x) for x in size.split("x")]
        cloth[left_offset:left_offset + width, upper_offset:upper_offset + height] += 1

    print(sum(sum(cloth > 1)))


def day3b():
    import numpy as np

    cloth = np.zeros([1000, 1000])

    with open("day_3_AOC") as fh:
        data = fh.readlines()

    def parse_request(request):
        requestnr, _, offsets, size = request.strip().split(" ")
        requestnr = int(requestnr.strip("#"))
        left_offset, upper_offset = [int(x) for x in offsets.strip(":").split(",")]
        width, height = [int(x) for x in size.split("x")]
        return [requestnr, left_offset, upper_offset, width, height]

    for request in data:
        requestnr, left_offset, upper_offset, width, height = parse_request(request)
        cloth[left_offset:left_offset + width, upper_offset:upper_offset + height] += 1

    for request in data:
        requestnr, left_offset, upper_offset, width, height = parse_request(request)
        cloth[left_offset:left_offset + width, upper_offset:upper_offset + height] += 1
        if sum(sum(cloth[left_offset:left_offset + width, upper_offset:upper_offset + height])) == height * width:
            print(requestnr)

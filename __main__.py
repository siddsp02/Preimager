import argparse
import multiprocessing as mp
import time

from preimaging import compute_preimage

MAX_WORKERS = mp.cpu_count()

parser = argparse.ArgumentParser(
    description="Compute a preimage that results in a hash with a number of prefix zeros.",
)
parser.add_argument(
    "-t",
    "--text",
    metavar="",
    help="the text to append",
    required=True,
    type=str,
)
parser.add_argument(
    "-s",
    "--size",
    metavar="",
    help="the size of the string to prepend (default size is 10)",
    default=10,
    type=int,
)
parser.add_argument(
    "-z",
    "--zeros",
    metavar="",
    default=5,
    help="the number of prefix zeros that should be in the hash",
    type=int,
)
parser.add_argument(
    "--attempts",
    metavar="",
    help="the maximum number of attempts before ending execution",
    default=100_000,
    type=int,
)
group = parser.add_mutually_exclusive_group()
group.add_argument(
    "--parallelize",
    metavar="",
    action=argparse.BooleanOptionalAction,
    help="parallelize computation across cores.",
)
group.add_argument(
    "-j",
    "--jobs",
    metavar="",
    help="the number of jobs/processes to parallelize computation",
    default=1,
    type=int,
)
args = parser.parse_args()
result = None
if args.parallelize or args.jobs > 1:
    if args.jobs > MAX_WORKERS:
        raise ValueError("Can't have more processes than cores.")
    elif args.parallelize:
        workers = MAX_WORKERS
    else:
        workers = args.jobs
    args.attempts //= workers
    s = time.perf_counter()
    with mp.Pool(workers) as pool:
        function_args = [(args.text, args.size, args.zeros, args.attempts)] * workers
        results = pool.starmap(compute_preimage, function_args)
        for value in results:
            if value is not None:
                result = value
                pool.terminate()
                break
else:
    s = time.perf_counter()
    result = compute_preimage(args.text, args.size, args.zeros, args.attempts)

print(result)
e = time.perf_counter()
print(f"Finished in {e-s:.8f} seconds.")

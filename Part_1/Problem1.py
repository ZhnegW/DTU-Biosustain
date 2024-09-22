from multiprocessing import Pool, cpu_count

def square(num):
    return num * num

def process_records(records):

    num_workers = cpu_count()

    with Pool(num_workers) as pool:
        results = pool.map(square, records)

    return results

if __name__ == "__main__":
    records = range(1000001)
    processed_results = process_records(records)
    print(f'Processed results: {processed_results[:10]}...')
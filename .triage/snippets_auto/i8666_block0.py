    try:
        matching_results = bmrt_cache["by_benchmark_name"][bname]
    except KeyError:
        return f"benchmark name not known: `{bname}`"

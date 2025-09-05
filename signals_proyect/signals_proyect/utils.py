import logging

def setup_logger():
    logging.basicConfig(filename='signals.log', level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s')

def percent(val, ref):
    try:
        return f"{(100 * (val - ref) / ref):.2f}%"
    except Exception:
        return "-" 
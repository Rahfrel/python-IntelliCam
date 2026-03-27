def count_objects(detected_labels):
    counts = {label: detected_labels.count(label) for label in set(detected_labels)}
    return counts
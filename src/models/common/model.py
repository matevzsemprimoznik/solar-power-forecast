def save_onnx_metadata(onnx_model, metadata):
    for item in metadata.items():
        m = onnx_model.metadata_props.add()
        m.key = item[0]
        m.value = item[1]

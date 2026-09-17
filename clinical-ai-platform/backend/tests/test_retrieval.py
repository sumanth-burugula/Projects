from app.vector_retrieval import vector_retrieve


def test_vector_retrieval_returns_patient_documents():
    documents = vector_retrieve("SYN-1001", "A1C diabetes laboratory")
    assert documents
    assert any("A1C" in document for document in documents)


def test_vector_retrieval_unknown_patient():
    assert vector_retrieve("UNKNOWN", "diabetes") == []

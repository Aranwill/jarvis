from jarvis.core.request import Request
from jarvis.kernel.kernel import Kernel


def test_kernel_returns_response():

    kernel = Kernel()

    request = Request(
        content="Hola Jarvis",
        session_id="test-session",
    )

    response = kernel.receive(request)

    assert response.content == "Hola Jarvis"
    assert response.source == "kernel"

def test_kernel_rejects_empty_request():

    kernel = Kernel()

    request = Request(
        content="",
        session_id="test-session",
    )

    response = kernel.receive(request)

    assert response.content == "La solicitud está vacía."
    assert response.source == "kernel"


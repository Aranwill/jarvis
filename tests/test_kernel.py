from malak.core.request import Request
from malak.kernel.kernel import Kernel


def test_kernel_returns_response():

    kernel = Kernel()

    request = Request(
        content="Hola Mundo",
        session_id="test-session",
    )

    response = kernel.receive(request)

    assert response.content == "Hola Mundo"
    assert response.source == "echo"

def test_kernel_rejects_empty_request():

    kernel = Kernel()

    request = Request(
        content="",
        session_id="test-session",
    )

    response = kernel.receive(request)

    assert response.content == "La solicitud está vacía."
    assert response.source == "kernel"

def test_kernel_dispatches_echo_capability():

    kernel = Kernel()

    request = Request(
        content="Malāk",
        session_id="dispatch-test",
    )

    response = kernel.receive(request)

    assert response.content == "Malāk"
    assert response.source == "echo"
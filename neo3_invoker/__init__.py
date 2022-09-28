import abc
from typing_extensions import NotRequired, TypedDict
from typing import Any
from neo3.network.payloads import verification


class Signer(TypedDict):
    scopes: verification.WitnessScope
    account: NotRequired[str]
    allowed_contracts: NotRequired[list[str]]
    allowed_groups: NotRequired[list[str]]


class ContractInvocation(TypedDict):
    script_hash: str
    operation: str
    args: list[Any]
    abort_on_fail: NotRequired[bool]


class ContractInvocationMulti(TypedDict):
    signers: list[Signer]
    invocations: list[ContractInvocation]
    extra_system_fee: NotRequired[int]
    system_fee_override: NotRequired[int]
    extra_network_fee: NotRequired[int]
    network_Fee_override: NotRequired[int]


class Neo3Invoker(abc.ABC):

    @abc.abstractmethod
    async def invoke_function(self, cim: ContractInvocationMulti) -> str:
        pass

    @abc.abstractmethod
    async def test_invoke(self, cim: ContractInvocationMulti) -> str:
        pass
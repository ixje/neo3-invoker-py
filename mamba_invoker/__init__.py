from neo3_invoker import Neo3Invoker, ContractInvocationMulti, Signer
from neo3 import vm
from neo3.api import NeoRpcClient
from neo3.core import types
from neo3.network.payloads import verification
from neo3.wallet import account
from typing import Optional
from dataclasses import dataclass

@dataclass
class RpcConfig:
    rpc_address: str
    network_magic: int


class MambaInvoker(Neo3Invoker):
    MAINNET = 'https://mainnet1.neo.coz.io:443'
    TESTNET = 'https://testnet1.neo.coz.io:443'

    def __init__(self, rpc_config: RpcConfig, account: Optional[account.Account] = None):
        self.config = rpc_config
        self.account = account

    @classmethod
    async def init(cls, rpc_address: str, account: Optional[account.Account] = None):
        async with NeoRpcClient(rpc_address) as client:
            res = await client.get_version()
            return cls(RpcConfig(rpc_address, res.protocol.network), account)

    async def test_invoke(self, cim: ContractInvocationMulti) -> str:
        sb = vm.ScriptBuilder()

        for invocation in cim['invocations']:
            hash = types.UInt160.from_string(invocation['script_hash'])
            operation = invocation['operation']
            # TODO: convert args
            args = invocation['args']
            abort = invocation.get('abort_on_fail', False)

            sb.emit_contract_call_with_args(hash, operation, args)
            if abort:
                sb.emit(vm.OpCode.ABORT)

        signers = list(map(lambda s: self._convert_signer(s), cim['signers']))
        async with NeoRpcClient(self.config.rpc_address) as client:
            result = await client.invoke_script(sb.to_array(), signers)
            # TODO: we can't print ExucutionResult as string, so doing this for now
            return str(result.state)

    def invoke_function(self, cim: ContractInvocationMulti) -> str:
        pass

    def _convert_signer(self, signer: Signer) -> verification.Signer:
        account = types.UInt160.from_string(signer['account'])
        # TODO: parse groups, contracts
        return verification.Signer(account, signer['scopes'])

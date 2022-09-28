import asyncio
from mamba_invoker import MambaInvoker
from neo3_invoker import ContractInvocation, Signer, ContractInvocationMulti
from neo3.wallet import account
from neo3.network.payloads.verification import WitnessScope
from neo3.contracts.contract import CONTRACT_HASHES


async def main():
    acct = account.Account.watch_only_from_address('NKuyBkoGdZZSLyPbJEetheRhMjeznFZszf')
    mamba_invoker = await MambaInvoker.init(MambaInvoker.MAINNET, acct)

    c: ContractInvocation = {
        "script_hash": str(CONTRACT_HASHES.NEO_TOKEN),
        "operation": "symbol",
        "args": []
    }
    # Note: cannot create ContractInvocation in place, because IDE doesn't understand the auto-complete
    invocations: list[ContractInvocation] = [c]

    s: Signer = {"account": str(acct.script_hash),
                 "scopes": WitnessScope.GLOBAL
                 }
    # Note: same here, cannot create Signer dicts in place, have to create instances above if you want to have auto-completion
    signers: list[Signer] = [s]


    formattedRequest: ContractInvocationMulti = {
        "invocations": invocations,
        "signers": signers
    }
    resp = await mamba_invoker.test_invoke(formattedRequest)
    print(resp)

if __name__ == '__main__':
    asyncio.run(main())
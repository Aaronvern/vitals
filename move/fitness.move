module FormFitRewards {
    use aptos_framework::coin;
    use aptos_framework::signer;

    struct FormFitToken has key {}

    public entry fun mint_reward(account: &signer, amount: u64) {
        coin::mint<FormFitToken>(account, amount);
    }
}
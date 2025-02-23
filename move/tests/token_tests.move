#[test_only]
module FormFitRewards::TokenTests {
    use FormFitRewards::FormFitToken;
    use aptos_framework::coin;

    #[test(account = @FormFitRewards, recipient = @0x2)]
    fun test_initialize_and_mint(account: &signer, recipient: &signer) {
        FormFitToken::initialize(account);
        FormFitToken::register(recipient);
        FormFitToken::mint_reward(account, @0x2, 100);
        assert!(coin::balance<FormFitToken::FormFitToken>(@0x2) == 100, 1);
    }
}
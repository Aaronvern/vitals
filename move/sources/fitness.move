module FormFitRewards::FormFitToken {
    use std::signer;
    use aptos_framework::coin;
    use std::string;

    struct FormFitToken has key {}

    struct MintCap has key {
        cap: coin::MintCapability<FormFitToken>,
    }

    public entry fun initialize(account: &signer) {
        let (burn_cap, freeze_cap, mint_cap) = coin::initialize<FormFitToken>(
            account,
            string::utf8(b"FormFit Token"),
            string::utf8(b"FFT"),
            6,
            true
        );
        move_to(account, MintCap { cap: mint_cap });
        coin::destroy_burn_cap(burn_cap);
        coin::destroy_freeze_cap(freeze_cap);
    }

    public entry fun mint_reward(account: &signer, recipient: address, amount: u64) acquires MintCap {
        let admin_addr = signer::address_of(account);
        assert!(exists<MintCap>(admin_addr), 1);
        let mint_cap = borrow_global<MintCap>(admin_addr);
        let coins = coin::mint<FormFitToken>(amount, &mint_cap.cap);
        coin::deposit(recipient, coins);
    }

    public entry fun register(account: &signer) {
        let addr = signer::address_of(account);
        if (!coin::is_account_registered<FormFitToken>(addr)) {
            coin::register<FormFitToken>(account);
        }
    }
}
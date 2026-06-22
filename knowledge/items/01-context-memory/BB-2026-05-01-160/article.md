# The DPoP Storage Paradox: Why Browser-Based Proof-of-Poss...

- BestBlogs URL: https://www.bestblogs.dev/en/article/ef3084e8
- Extraction: DOM text from BestBlogs page via OpenCLI browser bridge
- Extracted chars: 21261
- Original publisher URL: https://www.infoq.com/articles/dpop-key-storage-unsolved-problem/?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=global

---

Key Takeaways
DPoP (RFC 9449) prevents token replay by binding tokens to a client key pair, but the spec is silent on browser key storage, creating a security gap that practitioners must solve themselves.
Non-extractable CryptoKeys in IndexedDB do not prevent XSS exploitation; attackers can invoke crypto.subtle.sign() to proxy-sign DPoP proofs without ever extracting the private key.
The Backend-for-Frontend (BFF) pattern is the current industry standard for browser-based sender-constrained tokens, shifting key material server-side at the cost of infrastructure overhead.
For deployments where a BFF is infeasible, a memory-only key approach limits the XSS blast radius to a single non-persistent browser session.
No single pattern solves the storage paradox universally; architects must weigh deployment constraints, threat model, and operational maturity to choose.

Your security team just finished a DPoP integration. Private keys are stored in IndexedDB as non-extractable CryptoKey objects, which makes exportKey() throw an exception. The raw key bytes can't leave the browser. Everything passes the audit checklist — until a penetration tester drops an XSS payload that signs arbitrary DPoP proofs with your "protected" key and walks through your resource server without resistance. The key was never extracted. It didn't need to be.

This scenario captures a tension at the heart of OAuth 2.0's newest sender-constraining mechanism, as we will see in the next section. DPoP works as specified. The Web Crypto API works as specified. And yet the security guarantee that most teams assume they're getting from their combination doesn't exist in a browser context.

From Bearer Tokens to Proof-of-Possession

Bearer tokens have a well-known problem: anyone who possesses the token can use it. Exfiltration routes, including compromised logs, malicious browser extensions, XSS, open redirector chains, mean that possessing a token is often easier than it should be.

RFC 9700 (January 2025), the IETF's updated Best Current Practice for OAuth 2.0 security, identifies sender-constrained tokens as a recommended countermeasure against stolen token misuse. DPoP (RFC 9449, September 2023) is the application-layer mechanism that makes this practical for browser-based clients without requiring mutual TLS (mTLS) or transport-layer token binding, two advanced security mechanisms used to prevent token theft and replay attacks.

Mutual TLS achieves sender-constraining at the transport layer, but it requires client certificate infrastructure that browsers don't expose for application-level token binding. HTTP Token Binding (RFC 8471) was a parallel transport-layer effort, but Chrome removed support in late 2018 and no other major browser shipped it, leaving the standard effectively dead for browser clients.

Instead, DPoP works entirely at the application layer. The client generates an asymmetric key pair, then signs a DPoP proof JWT for each request. The proof header declares typ: dpop+jwt, the signing algorithm, and the client's public key in JWK format. The payload binds the proof to the HTTP method (htm), target URI (htu), a unique identifier (jti), and a timestamp (iat). The authorization server validates the proof and issues an access token containing a cnf claim with the JWK Thumbprint of the client's public key — "cnf": {"jkt": "<thumbprint>"} — tying the token to the key that requested it.

When the client presents the bound token to a resource server, it sends a fresh DPoP proof alongside it. The proof includes an ath claim — a hash of the access token — binding this specific proof to this specific token. The resource server verifies the proof signature, confirms the htm and htu match the incoming request, and checks that the jkt in the access token matches the proof's public key. Only then does it honor the request. A stolen token is useless without the corresponding private key to produce valid proofs.

Figure 1: The DPoP flow. Each request requires a fresh proof signed by the client's private key, binding the token to the key that requested it.

Ecosystem adoption is accelerating. Spring Security 6.5 added DPoP support in May 2025. Keycloak 26.4 shipped it in September 2025. Auth0 shipped DPoP as generally available on Enterprise plans in March 2026. The OpenID Foundation's FAPI 2.0 Security Profile, finalized in February 2025, mandates sender-constrained tokens for financial-grade APIs, positioning DPoP as the practical sender-constraining mechanism for any FAPI 2.0 deployment where mTLS infrastructure is unavailable. The protocol is no longer theoretical — teams are implementing it now. Which raises a question RFC 9449 leaves entirely to the implementer: in a browser, where does the private signing key actually live, and how do you keep it safe from the very scripts that need to use it? The next section unpacks that tension.

The Browser Constraint: Where the Specification Ends and the Trouble Begins

RFC 9449 tells the client to "generate" a key pair. It says nothing about where to store it. For server-side clients, this is a non-issue — the key lives in process memory on a machine the attacker can't reach. For a browser-based SPA, the question has no clean answer.

localStorage and sessionStorage cannot store CryptoKey objects at all. The key must be serialized as an extractable JWK — a plain JSON string sitting in a storage area fully accessible to any script running on the same origin. XSS steals the raw key material in one line.

IndexedDB with a non-extractable CryptoKey is the approach recommended by draft-ietf-oauth-browser-based-apps-26 (Section 6.3.4.2.2), the IETF's near-BCP guidance for browser-based OAuth clients. The Web Crypto API lets you generate a key pair where the private key's extractable property is false. IndexedDB can store the resulting CryptoKey object via the structured clone algorithm. Calling exportKey() on this key throws an InvalidAccessError. So far, so good.

Web Workers can isolate refresh tokens from the main thread's window scope (draft-ietf-oauth-browser-based-apps-26, Section 6.3.4.2.1), but they do not create a trust boundary for the signing key. Any script running on the same origin can postMessage the Worker to request a signature. The access token and the signing key remain reachable from any code on the page.

Here's the part that catches teams off guard: the extractable property gates exactly two operations: exportKey() and wrapKey(). That is all. The Web Crypto specification says nothing about preventing sign(). A non-extractable key is a key whose bytes you cannot export. It is not a key that cannot be used.

This creates a cognitive trap. The exportKey() rejection leads developers to reasonably (but incorrectly) assume that a key which cannot be exported is also a key which cannot be misused. The API is behaving exactly as specified. The gap is in the developer's mental model, not the browser's behavior. This is the storage paradox: the browser provides no mechanism that makes a key both usable for signing and safe from script-level abuse.

The distinction is two lines of code:

await crypto.subtle.exportKey('jwk', privateKey);  // throws InvalidAccessError
await crypto.subtle.sign(alg, privateKey, payload); // succeeds — valid signature

Testing the first does not guarantee that an attacker cannot use the second.

The Oracle Attack

An attacker who achieves XSS on your SPA's origin does not need to extract the key. They just need access to the machine that holds it. The attack works like this:

Injected script opens an IndexedDB transaction and reads the stored CryptoKey handle
The script calls crypto.subtle.sign() with that handle, an attacker-controlled header, and an attacker-controlled payload
The result is a valid DPoP proof JWT — correctly signed, for any HTTP method and any target URI the attacker chooses
The attacker attaches this proof to the stolen access token and calls the resource server directly, or proxies the request through the victim's browser.

The browser's crypto subsystem becomes a signing oracle. The attacker never touches the raw key bytes. Again, they don't need to.

Figure 2: The Oracle Attack. XSS uses the browser's own crypto subsystem as a signing oracle without extracting the private key.

DPoP nonces (RFC 9449, Section 8) let the authorization server control proof freshness: the server issues a nonce, the client must include it in the next proof, preventing replay of intercepted proofs. But nonces do not change the Oracle Attack calculus: the attacker generates each proof on demand with the current nonce, producing valid, non-replayable proofs in real time.

This isn't a theoretical concern. Draft-ietf-oauth-browser-based-apps-26, Section 5.2.2 states that with DPoP, "the attacker can only abuse stolen application tokens by carrying out an online attack, where the proofs are calculated in the user's browser," and refers readers to RFC 9449, Section 11.4 ("Untrusted Code in the Client Context") for details. §11.4 is unambiguous: if an adversary can execute code in the client's origin, "the adversary can...create new DPoP proofs as long as the client is online" — regardless of non-extractability. The mitigations the RFC recommends are secure coding practices to prevent XSS, plus Content Security Policy as a second layer of defense. Both sit outside the protocol. The same document that recommends IndexedDB storage therefore documents, in its own security considerations, an attack the protocol itself cannot close.

Cross-browser inconsistencies sharpen the problem. Firefox cannot store CryptoKey objects in IndexedDB at all; the structured clone algorithm fails with a DOMException (Bugzilla #1348279, RESOLVED WONTFIX). The only workaround is to export the key to JWK format, which requires extractable: true, completely defeating non-extractability. Firefox doesn't just fail to mitigate the Oracle Attack — it forces a strictly worse security posture. Separately, some browsers silently drop IndexedDB data in private browsing modes, adding another failure path for key persistence.

These constraints leave browser-based DPoP implementations in a bind. The recommended storage approach is vulnerable to the Oracle Attack in Chromium browsers and outright broken in Firefox. This is why the industry has largely converged on moving the problem out of the browser entirely.

The BFF Pattern: The Current Industry Standard

The IETF's guidance for browser-based applications (draft-ietf-oauth-browser-based-apps-26) presents its architectural patterns "in decreasing order of security." The Backend-for-Frontend pattern comes first — the draft's top-ranked architecture for browser-based OAuth.

The pattern restructures the trust boundary. Instead of the SPA acting as a public OAuth client, a server-side component, the BFF, acts as a confidential client. The BFF generates the DPoP key pair in its own process memory, handles the authorization code exchange with client credentials, manages access and refresh tokens, and produces DPoP proofs for each outbound API request. The browser never sees key material or tokens. It holds only an HTTP-only, Secure, SameSite cookie that maps to the BFF's session.

Figure 3: The trust boundary shift. With a BFF, key material and tokens never reach the browser.

The security improvement is categorical, not incremental. XSS on the SPA can still proxy requests through the victim's active browser session. But the attack surface shrinks dramatically: the attacker cannot extract tokens, cannot forge DPoP proofs, and cannot invoke crypto.subtle.sign() because there is no CryptoKey in the browser to sign with. When the session cookie expires or the user closes the browser, the attacker's access ends with it.

The BFF also prevents a harder attack that client-side DPoP cannot address at all. Draft-ietf-oauth-browser-based-apps-26, Section 5.1.3, describes the fresh token acquisition attack: XSS launches a silent Authorization Code flow in a hidden iframe, generates the attacker's own DPoP key pair, and obtains entirely new tokens bound to that key. The attacker doesn't need your keys. They mint their own. Because the BFF is a confidential client, the authorization code exchange requires client credentials the attacker doesn't have. This is the strongest argument for the BFF model: it closes attack vectors that no amount of client-side cryptographic hardening can address.

Real-world adoption reflects the consensus. Duende provides a production BFF framework for .NET, with DPoP proof generation built into the proxy layer. Spring Cloud Gateway handles the pattern via OAuth2 token relay filters. Auth.js (formerly NextAuth.js) wraps it for Node.js. On the authorization server side, Keycloak 26.4 supports selective refresh-token-only DPoP binding, where only the refresh token is sender-constrained while access tokens remain bearer, reducing per-request overhead while protecting the most sensitive credentials. This aligns with draft-rosomakho-oauth-dpop-rt-00, an IETF draft on separating DPoP bindings for access and refresh tokens (readers should check the IETF datatracker for successor documents, as the draft expires in April 2026).

Trade-offs

The trade-offs are real and worth stating plainly. A BFF is an additional infrastructure component to deploy, scale, and monitor. It adds a network hop between the SPA and the resource server, measurable in latency-sensitive applications. Session management reintroduces cookie-based CSRF considerations that many teams thought they'd left behind with token-based auth. Shared or sticky sessions add operational complexity.

For some deployment models, a BFF isn't just costly — it's impossible. Browser extensions have no server at all. Third-party widgets embedded in another organization's page have no control over the host's backend. Offline-first PWAs on CDN-only infrastructure may face contractual constraints against server-side compute. Edge functions have made BFFs easier to deploy in general, but these specific cases remain genuinely serverless.

Case Study: A "Zero-Persistence" Approach for Constrained Deployments

In this section, we will explore an alternative approach that mitigates the risk associated with DPoP for scenarios where BFF is not an option.

For one such project my team executed, a headless authentication layer serving browser extensions with no backend, we initially reached for the IndexedDB approach. Firefox's CryptoKey serialization failure killed that path in cross-browser testing within the first week.

That failure led us to explore a different constraint: what if the key pair never touches persistent storage at all?

The memory-only lifecycle. The DPoP key pair is generated via crypto.subtle.generateKey() with extractable: false and held in a module-scoped JavaScript variable. It is never written to IndexedDB, localStorage, or any other persistent store. When the page reloads, the tab closes, or the user navigates away, the key is gone.

// toBase64Url: standard Base64URL encoding per RFC 4648 §5 (omitted for brevity)
const keyPair = await crypto.subtle.generateKey(
  { name: 'ECDSA', namedCurve: 'P-256' },
  false,  // private key non-extractable
  ['sign', 'verify']
);

async function createDpopProof(method, url) {
  const header = { alg: 'ES256', typ: 'dpop+jwt',
                    jwk: await crypto.subtle.exportKey('jwk', keyPair.publicKey) };
  const payload = { htm: method, htu: url, iat: Math.floor(Date.now() / 1000),
                    jti: crypto.randomUUID() };
  const signingInput = toBase64Url(JSON.stringify(header))
                     + '.' + toBase64Url(JSON.stringify(payload));
  const sig = await crypto.subtle.sign(
    { name: 'ECDSA', hash: 'SHA-256' }, keyPair.privateKey,
    new TextEncoder().encode(signingInput));
  return signingInput + '.' + toBase64Url(sig);
}

An attacker who achieves XSS can still access the in-memory handle and invoke sign() during the current session — the Oracle Attack applies here too. But the blast radius changes. The key cannot survive a page reload. The attacker cannot establish a persistent foothold across sessions. Combined with a strict Content Security Policy (no unsafe-inline, no unsafe-eval), the attack window shrinks to the lifetime of the injected script's execution context.

The Lazy Re-Binding handshake. A key that dies on every page reload would force re-authentication on every refresh, which is unworkable for any app a user keeps open. Lazy Re-Binding is the corollary mechanism that makes memory-only practical: on page reload, the client generates a fresh key pair and presents its refresh token alongside a new DPoP proof signed with the new key. The authorization server validates the refresh token, issues a new access token bound to the new public key, and invalidates the old binding. The key rotates as a routine consequence of normal browser behavior, not as a security event. This requires the authorization server to support DPoP key rotation on token refresh — not universally supported today, though draft-rosomakho-oauth-dpop-rt-00 (under active IETF discussion as of this writing) outlines a mechanism that enables exactly this class of key rotation pattern.

Figure 4: The Lazy Re-Binding handshake. After a page reload destroys the old key, the client re-establishes trust with a fresh key pair.

The blast radius shrinks but the attack surface does not. The fresh token acquisition attack (draft-ietf-oauth-browser-based-apps-26, Section 5.1.3) applies to the zero-persistence model just as it applies to any public client architecture. An XSS attacker can launch a silent Authorization Code flow, generate their own key pair, and obtain fresh tokens, completely bypassing the application's keys. Only a confidential client (BFF) prevents this. The zero-persistence approach narrows the Oracle Attack window; it does not close the public-client attack surface.

Multi-tab coordination is a correctness requirement, not an optimization. If Tab A reloads and generates a new key, the server rotates the DPoP binding. Tab B still holds the old key. Tab B's proofs fail. Without a coordination mechanism like BroadcastChannel or SharedWorker to propagate the new key across tabs, the application breaks in a routine user scenario.

A strict CSP is a hard prerequisite. Authorization server support for proof key rotation is required. And this is not a replacement for BFF when BFF is feasible. It is an alternative for the specific deployment constraints where it isn't.

Choosing the Right Pattern

No silver bullet exists. The decision depends on what your architecture can support and which threats you prioritize.

BFF Pattern. Best for teams with existing backend infrastructure, regulatory requirements for server-side token management, or low tolerance for browser-side risk. Prevents both the Oracle Attack and the fresh token acquisition attack. Trade-off: infrastructure and latency overhead.
Memory-Only / Zero-Persistence. Viable for browser extensions, embedded widgets, CDN-only static sites, or teams with mature CSP and tolerance for short-lived sessions. Limits persistent Oracle Attack exposure. Trade-off: same-session XSS remains effective; multi-tab coordination is required; fresh token acquisition is not prevented.
IndexedDB with non-extractable keys. Acceptable when combined with defense-in-depth — strict CSP, Subresource Integrity, and Trusted Types (available in Chromium 83+ and Safari 26+, though notably still behind a flag in Firefox). The team must accept the Oracle Attack as a residual risk.
Hybrid. Some teams combine a lightweight BFF for token management with client-side DPoP for API-level sender-constraining. Worth watching as the ecosystem matures.
What Comes Next

DPoP closes a real gap in OAuth 2.0. Sender-constrained tokens are a meaningful upgrade over bearer tokens for any client that can implement them. But RFC 9449's silence on browser key storage creates the need for an architectural decision that each team must confront deliberately — there is no safe default that works everywhere.

The BFF pattern is the safest choice today for browser-based applications. Memory-only approaches show promise for genuinely constrained deployments but carry trade-offs that demand mature operational practices and rigorous threat modeling.

The ecosystem is moving. Firefox's CryptoKey-in-IndexedDB gap remains an open frustration. Authorization server support for DPoP key rotation is expanding. Trusted Types provide a defense-in-depth layer that reduces XSS risk at the injection point, though Firefox's delayed adoption mirrors the same cross-browser gap that complicates CryptoKey storage. The W3C's Web Cryptography Level 2 (FPWD, April 2025) extends the API but adds no dedicated key isolation mechanism. Device Bound Session Credentials (DBSC), which demonstrated TPM-backed key isolation in Chrome trials on Windows, represent the most promising long-term signal — if DBSC matures and reaches broad browser support, the storage paradox may find a native resolution.

Until then, the paradox stands. DPoP gives you proof-of-possession. The browser gives you nowhere safe to put what you possess.

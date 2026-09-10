export async function onRequestPost(context) {
  try {
    const { request, env } = context;
    let email = '', items = [], promo = '';
    const ct = request.headers.get('content-type') || '';
    if (ct.includes('application/json')) {
      const b = await request.json();
      email = (b.email || '').trim();
      if (Array.isArray(b.items)) items = b.items.slice(0, 12).map(x => String(x).slice(0, 80));
      promo = String(b.promo || '').slice(0, 40);
    } else {
      const f = await request.formData(); email = (f.get('email') || '').trim();
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email))
      return new Response(JSON.stringify({ ok: false, error: 'invalid_email' }), { status: 400, headers: { 'content-type': 'application/json' } });

    const H = { 'api-key': env.BREVO_KEY, 'content-type': 'application/json' };
    const attributes = { SOURCE: 'thealdera.com prelaunch' };
    if (items.length) {
      attributes.PREORDER = items.join(' | ');
      attributes.PROMO = promo || 'FOUNDING25';
      attributes.PREORDER_AT = new Date().toISOString();
    }
    // 1) store contact (idempotent)
    await fetch('https://api.brevo.com/v3/contacts', {
      method: 'POST', headers: H,
      body: JSON.stringify({ email, updateEnabled: true, attributes })
    });
    // 2) notify inbox
    const isPO = items.length > 0;
    await fetch('https://api.brevo.com/v3/smtp/email', {
      method: 'POST', headers: H,
      body: JSON.stringify({
        sender: { name: 'The Aldera Site', email: 'aleksor@thealdera.com' },
        to: [{ email: 'info@thealdera.com' }],
        subject: (isPO ? 'New PRE-ORDER reservation: ' : 'New launch-list signup: ') + email,
        textContent: (isPO ? 'New pre-order reservation on thealdera.com\n\n' : 'New signup on thealdera.com\n\n')
          + 'Email: ' + email + '\n'
          + (isPO ? 'Items: ' + items.join(', ') + '\nPromo: ' + (promo || 'FOUNDING25') + '\n' : '')
          + 'Time: ' + new Date().toISOString()
      })
    });
    return new Response(JSON.stringify({ ok: true }), { headers: { 'content-type': 'application/json' } });
  } catch (e) {
    return new Response(JSON.stringify({ ok: false, error: 'server' }), { status: 500, headers: { 'content-type': 'application/json' } });
  }
}

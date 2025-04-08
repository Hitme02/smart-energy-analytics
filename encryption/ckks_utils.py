import tenseal as ts

def get_ckks_context():
    context = ts.context(
        ts.SCHEME_TYPE.CKKS,
        poly_modulus_degree=8192,
        coeff_mod_bit_sizes=[60, 40, 40, 60]
    )
    context.global_scale = 2**40
    context.generate_galois_keys()
    return context

def encrypt_value(context, value):
    return ts.ckks_vector(context, [value])

def decrypt_value(context, enc_val):
    return enc_val.decrypt()[0]

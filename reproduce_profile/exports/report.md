# Extraction Report
- Profile path: d:\vehicle\37ab1612-c285-4314-b32a-6a06d35d6d84

- Failed to extract Local State key. Some decryption may fail.
- Cookies exported: 367 rows -> d:\vehicle\reproduce_profile\exports\cookies.csv
- Logins exported: 2 rows -> d:\vehicle\reproduce_profile\exports\logins.csv
- Web Data exported: autofill 2, credit_cards 0, addresses 0
- Raw files saved: 2 -> d:\vehicle\reproduce_profile\exports\raw_files

## Summary
- Cookies: 367
- Logins: 2
- Autofill rows: 2
- Credit cards found: 0
- Addresses found: 0
- Raw files saved: 2

## Errors & Notes
- dpapi_ctypes_exception: argument 1: OverflowError: int too long to convert
- powershell_dpapi_failed: Unable to find type [System.Security.Cryptography.ProtectedData].
At line:1 char:34
+ ... ::ToBase64String([System.Security.Cryptography.ProtectedData]:
:Unprot ...
+                      ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidOperation: (System.Security... 
   y.ProtectedData:TypeName) [], RuntimeException
    + FullyQualifiedErrorId : TypeNotFound
- local_state_key: PowerShell DPAPI failed: Unable to find type [System.Security.Cryptography.ProtectedData].
At line:1 char:34
+ ... ::ToBase64String([System.Security.Cryptography.ProtectedData]:
:Unprot ...
+                      ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidOperation: (System.Security... 
   y.ProtectedData:TypeName) [], RuntimeException
    + FullyQualifiedErrorId : TypeNotFound
- dpapi_ctypes_failed: CryptUnprotectData returned 87
- powershell_dpapi_failed: Unable to find type [System.Security.Cryptography.ProtectedData].
At line:1 char:34
+ ... ::ToBase64String([System.Security.Cryptography.ProtectedData]:
:Unprot ...
+                      ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidOperation: (System.Security... 
   y.ProtectedData:TypeName) [], RuntimeException
    + FullyQualifiedErrorId : TypeNotFound
- dpapi_decrypt: PowerShell DPAPI failed: Unable to find type [System.Security.Cryptography.ProtectedData].
At line:1 char:34
+ ... ::ToBase64String([System.Security.Cryptography.ProtectedData]:
:Unprot ...
+                      ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidOperation: (System.Security... 
   y.ProtectedData:TypeName) [], RuntimeException
    + FullyQualifiedErrorId : TypeNotFound
- dpapi_ctypes_failed: CryptUnprotectData returned 87
- powershell_dpapi_failed: Unable to find type [System.Security.Cryptography.ProtectedData].
At line:1 char:34
+ ... ::ToBase64String([System.Security.Cryptography.ProtectedData]:
:Unprot ...
+                      ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidOperation: (System.Security... 
   y.ProtectedData:TypeName) [], RuntimeException
    + FullyQualifiedErrorId : TypeNotFound
- dpapi_decrypt: PowerShell DPAPI failed: Unable to find type [System.Security.Cryptography.ProtectedData].
At line:1 char:34
+ ... ::ToBase64String([System.Security.Cryptography.ProtectedData]:
:Unprot ...
+                      ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidOperation: (System.Security... 
   y.ProtectedData:TypeName) [], RuntimeException
    + FullyQualifiedErrorId : TypeNotFound
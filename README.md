# Darktable GraphQL API

A GraphQL API to access photos of your local
[Darktable](https://www.darktable.org/) library for use in other applications,
like a [static portfolio website](https://github.com/jonasberge/darktable-portfolio).
This removes the need to export photos by hand
and instead directly access them through an intuitive, programmable query interface.

Current and future features:
- Allows enumeration of photos and tags of a locally installed Darktable instance
- Exporting photos is done by downloading them from a well-defined URL path,
which is also shown in GraphQL objects
- Accesses the Darktable database in read-only mode only (modifications are not allowed)
- Exports on the fly and caches the result until XMP changes are made
- Implements the following security features, in case they are needed.
These can be used to make sure that e.g. a website frontend does not
show any full-resolution, high-quality photos
    - Restrict access to photos with specific tags
    - Restrict exports to specific formats only (like JPEG only)
    - Restrict export dimensions and quality to a certain value
- Allows full configuration of all `darktable-cli` parameters used

## Notes on the intended use

This API is generally not meant to be used as a public API,
which faces the internet.
It accesses a locally installed Darktable library,
and should only be used on the local host or a small, trusted network.
There is no plan to implement any security features
beyond the ones listed above,
which are more of a fail-safe anyway.

The intended use is to provide a well-designed and maintable interface
for e.g. a portfolio website which is statically generated
and does not depend on this API in a production environment.

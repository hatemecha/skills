# License selection and review

## Contents

1. Questions to answer
2. Common options
3. Terms that are not open source
4. Compatibility and third parties
5. Different types of repository content
6. Technical application
7. Primary references

## 1. Questions to answer

Before recommending a license, determine:

1. May others create proprietary derivative products?
2. Must distributed modifications remain open?
3. Should obligations cover modified software offered over a network?
4. Is an explicit patent grant important?
5. Is this a library intended to link with differently licensed software?
6. Are existing contributions or dependencies incompatible with the preferred license?
7. Does the project include documentation, assets, data, models, or trademarks?
8. Is dual licensing planned?

Do not choose a license only because it is popular.

## 2. Common options

### MIT

Choose MIT for a short, permissive license. It allows proprietary forks and requires preservation of the copyright and license notice. Its patent language is less explicit than Apache-2.0.

### Apache-2.0

Choose Apache-2.0 for a permissive license with an explicit patent grant and termination provisions. It allows proprietary forks and requires preservation of notices. A `NOTICE` file may also need to be retained.

### GPL-3.0-or-later

Choose GPL for strong copyleft on distributed derivative works. Compatible derivatives distributed to others must preserve the covered freedoms. Ordinary private network use does not generally trigger source distribution.

### AGPL-3.0-or-later

Choose AGPL when users interacting with a modified version over a network should also be able to obtain the corresponding source. This can reduce commercial adoption and requires careful architectural review.

### LGPL-3.0-or-later

Consider LGPL mainly for libraries when copyleft should cover the library without necessarily applying the same license to the complete program that uses it, subject to its conditions.

### MPL-2.0

Choose MPL as a middle ground with file-level copyleft. Modified covered files remain under MPL, while they can be combined with files under other licenses.

### Dual licensing

Offer the same code under two sets of terms, such as copyleft and commercial licenses, only when the project controls the necessary rights to all contributions or has suitable contributor agreements.

## 3. Terms that are not open source

Do not describe a license as open source when it prohibits commercial use, competition, specific industries, political or geographic groups, or use without prior approval. Time-limited source visibility without rights to modify and redistribute is source-available, not open source.

## 4. Compatibility and third parties

- Inventory direct dependencies, copied code, snippets, assets, models, datasets, and submodules.
- Read actual license terms rather than inferring them from a repository name.
- Preserve required notices and attribution.
- Do not relicense third-party contributions without legal authority.
- Document exceptions and vendored code.
- Treat automated scans as aids, not as substitutes for review.

## 5. Different repository content

A repository may require separate terms for:

- source code;
- documentation;
- visual or audio assets;
- data;
- model weights;
- trademarks and logos.

State these distinctions clearly. Opening the code does not automatically license every other asset.

## 6. Technical application

- Include the complete text in `LICENSE` or `LICENSES/`.
- Use valid SPDX identifiers.
- Keep package manifests consistent with repository terms.
- Add SPDX headers or per-file metadata when warranted.
- Consider the [REUSE Specification](https://reuse.software/spec/) for multiple rights holders or licenses.
- Preserve `NOTICE` and attribution files.
- Confirm that published packages include required license material.

Do not present the result as legal advice.

## 7. Primary references

- [OSI-approved licenses](https://opensource.org/licenses)
- [SPDX License List](https://spdx.org/licenses/)
- [SPDX guidance](https://spdx.dev/learn/handling-license-info/)
- [REUSE Specification](https://reuse.software/spec/)
- [GNU license recommendations](https://www.gnu.org/licenses/license-recommendations.html)

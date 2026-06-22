# Tplmap: Server-Side Template Injection and Code Injection Detection and Exploitation Tool

- Extraction: GitHub README excerpts
- BestBlogs URL: Not found during this capture
- Original publisher URL: https://github.com/epinna/tplmap

---

## Key Evidence

Tplmap assists SSTI detection and exploitation with a range of sandbox escape techniques. The README shows a black-box workflow from vulnerable parameter discovery to engine identification and capability discovery.

## Extracted Excerpts

- {{7*7}} rendering as 49 is used as a black-box indicator of SSTI.
- The tool reports engine, injection syntax, context, OS, technique, and capabilities.
- Capability outputs include shell command execution, file read, file write, and code evaluation.

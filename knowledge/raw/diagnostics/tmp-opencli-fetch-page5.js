(async () => {
  const url = 'https://www.bestblogs.dev/api/proxy/resources?page=5&pageSize=20&timeFilter=1w&language=all&sortType=latest&type=ARTICLE&qualifiedFilter=false&uiLang=en';
  const res = await fetch(url, { credentials: 'include' });
  const text = await res.text();
  console.log(text);
})();

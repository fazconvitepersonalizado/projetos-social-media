// Campos de texto editáveis de um carousel.html.
// Fonte única, usada por gerar_aprovacao.py, aplicar_respostas.py e pela
// página de aprovação: os três precisam numerar os textos do mesmo jeito.
//
// Regra: dentro de cada .ig-slide (na ordem do documento), um campo é
//  - um elemento com data-edit-id (padrão do editor do instagram-carousel); ou
//  - o bloco de texto mais externo que só tem filhos "inline" (span, em,
//    strong, br...). Esses ganham data-ap-id="slide{N}-t{i}".
// O texto vai para o editor com quebras de linha no lugar de <br> e com
// [[trechos]] marcando os destaques (span/em/strong), para que editar o
// texto não apague o estilo do destaque.
var APCampos = (function () {
  var INLINE = /^(SPAN|EM|STRONG|B|I|U|MARK|SMALL|SUP|SUB|A|BR)$/;

  function soInline(el) {
    if (!el.textContent.trim()) return false;
    var todos = el.querySelectorAll("*");
    for (var k = 0; k < todos.length; k++) {
      if (!INLINE.test(todos[k].tagName.toUpperCase())) return false;
    }
    return true;
  }

  // Duas convenções de carrossel convivem no projeto:
  // .ig-viewport/.ig-track/.ig-slide e .carousel-viewport/.carousel-track/.slide.
  function trilho(doc) {
    return doc.querySelector(".ig-track, .carousel-track");
  }

  function slides(doc) {
    var t = trilho(doc);
    return t ? Array.prototype.filter.call(t.children, function (el) {
      return !/^(SCRIPT|STYLE)$/i.test(el.tagName);
    }) : [];
  }

  function campos(doc) {
    var out = [];
    slides(doc).forEach(function (slide, i) {
      var n = i + 1, auto = 0, pegos = [];
      var els = slide.querySelectorAll("*");
      for (var k = 0; k < els.length; k++) {
        var el = els[k], tag = el.tagName.toUpperCase();
        if (tag === "SCRIPT" || tag === "STYLE" || el.closest("svg")) continue;
        if (pegos.some(function (p) { return p.contains(el); })) continue;
        var id = el.getAttribute("data-edit-id");
        if (id) {
          pegos.push(el);
          out.push({ id: id, slide: n, papel: id.replace(/^slide\d+-/, ""), el: el });
          continue;
        }
        if (el.closest("[data-edit-id]") || el.querySelector("[data-edit-id]")) continue;
        // Fora: contador de página ("1/7") e ícone solto (emoji sem letra nem número).
        var txt = el.textContent.trim();
        if (/^\d+\s*\/\s*\d+$/.test(txt) || !/[A-Za-zÀ-ÿ0-9]/.test(txt)) continue;
        if (soInline(el)) {
          auto++;
          var aid = "slide" + n + "-t" + auto;
          el.setAttribute("data-ap-id", aid);
          pegos.push(el);
          out.push({ id: aid, slide: n, papel: "texto " + auto, el: el });
        }
      }
    });
    return out;
  }

  function ler(el) {
    var s = "";
    el.childNodes.forEach(function (nd) {
      if (nd.nodeType === 3) s += nd.nodeValue.replace(/\s+/g, " ");
      else if (nd.nodeType === 1) {
        if (nd.tagName.toUpperCase() === "BR") s += "\n";
        else s += "[[" + nd.textContent.replace(/\s+/g, " ").trim() + "]]";
      }
    });
    return s.split("\n").map(function (l) { return l.trim(); }).join("\n").trim();
  }

  function moldes(el) {
    return Array.prototype.filter.call(el.childNodes, function (n) {
      return n.nodeType === 1 && n.tagName.toUpperCase() !== "BR";
    }).map(function (n) { return n.cloneNode(false); });
  }

  function escrever(el, valor, ms) {
    var doc = el.ownerDocument;
    while (el.firstChild) el.removeChild(el.firstChild);
    var k = 0;
    String(valor).split(/(\[\[[\s\S]*?\]\])/).forEach(function (parte) {
      if (!parte) return;
      var m = parte.match(/^\[\[([\s\S]*)\]\]$/);
      var alvo = el, txt = parte;
      if (m) {
        var base = ms && ms.length ? ms[Math.min(k, ms.length - 1)] : null;
        k++;
        if (base) { alvo = base.cloneNode(false); el.appendChild(alvo); }
        txt = m[1];
      }
      txt.split("\n").forEach(function (linha, j) {
        if (j) alvo.appendChild(doc.createElement("br"));
        if (linha) alvo.appendChild(doc.createTextNode(linha));
      });
    });
  }

  return { campos: campos, ler: ler, moldes: moldes, escrever: escrever, slides: slides, trilho: trilho };
})();

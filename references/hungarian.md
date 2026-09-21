# Magyar réteg

Az angol szabálylista nagy része átvihető, de három dolog nem: van néhány magyar AI-fordulat,
amit az angol lista nem ismer; van két angol szabály, ami magyarul **fordítva** igaz; és a magyar
mondatszerkezet másképp romlik el. A szerkezeti réteg (`narrative-structure.md`) nyelvfüggetlen,
azt magyarul is ugyanúgy kell alkalmazni.

A szöveg nyelvéhez igazodj, ne a kérés nyelvéhez. Magyar kérésre írt angol doksira az angol
szabályok érvényesek.

## Ami magyarul fordítva igaz

**Gondolatjel.** Az angol §14 kimondja, hogy a kész szövegben ne legyen em vagy en dash. Magyarul
ez hibás tanács: a gondolatjel (–, nagykötőjel, szóközökkel) szabályos magyar központozás, és a
kihagyása teszi géppé a szöveget, nem a használata. Amit magyarul javítani kell, az a rossz jel:
a kötőjel (-) gondolatjel helyett, és a hosszú kötőjel (—), ami a magyarban nem használatos.

- Rossz: `A vizsgálat - amiről korábban volt szó - lefutott.`
- Rossz: `A vizsgálat — amiről korábban volt szó — lefutott.`
- Jó: `A vizsgálat – amiről korábban volt szó – lefutott.`

**Idézőjel.** Az angol §19 a göndör idézőjelet kéri egyenesre cserélni. Magyarul a helyes alsó-
felső idézőjel „így néz ki”, a belső idézet »így«. Az egyenes " magyar prózában tipográfiai hiba,
nem emberi jel.

## Magyar AI-fordulatok

Ezek a magyar megfelelői az angol §7-nek (overused AI words). Csoportban jelennek meg, és a
csoport a tell, nem az egyes szó.

**Nyitó közhelyek:** napjainkban, a mai rohanó világban, a digitális korban, egyre inkább,
nem véletlen, hogy, mindannyian tudjuk, hogy, gondoltál már arra, hogy

**Felnagyítás:** elengedhetetlen, kulcsfontosságú, létfontosságú, kiemelkedő jelentőségű,
meghatározó szerepet játszik, alapvető fontosságú, nem elhanyagolható, rendkívül fontos

**Marketing:** átfogó megoldás, hatékony megoldás, testre szabott, letisztult, felhasználóbarát,
innovatív, prémium minőségű, gördülékeny, zökkenőmentes, a legmodernebb

**Kötőelemek, ha halmozódnak:** továbbá, emellett, ugyanakkor, mindazonáltal, ezen felül,
érdemes megjegyezni, hogy, fontos kiemelni, hogy

**Lezárás:** összességében elmondható, hogy; mindent egybevetve; remélhetőleg; a jövő fényes;
a lehetőségek tárháza szinte végtelen

Egy „továbbá” önmagában nem jel. Négy bekezdésnyi „továbbá – emellett – ugyanakkor” az.

## Szerkezeti magyar hibák

### Nominalizáció

A magyar AI-szöveg főnevesít, ahol az ember igét használ. Ez teszi hivatalos ízűvé.

- `a rendszer frissítésének elvégzése` → `frissítjük a rendszert`
- `a hiba javítására került sor` → `kijavítottuk a hibát`
- `a beállítások módosítása szükséges` → `át kell állítani a beállításokat`

### A „kerül” passzív

Magyarul nincs igazi szenvedő szerkezet, ezért az AI a „kerül” igével pótolja. Szinte mindig
cserélhető cselekvő alakra, és attól lesz emberi.

- `a jelentés kiküldésre kerül` → `kiküldjük a jelentést`
- `a domain ellenőrzésre kerül` → `ellenőrizzük a domaint`, vagy `a rendszer ellenőrzi a domaint`

Ha a cselekvő ismeretlen, mondd ki: `valaki átírta a DNS-rekordot`, ne `a rekord átírásra került`.

### Tükörfordított ritmus

Angol mondatszerkezet magyar szavakkal. Ez a legerősebb magyar AI-jel.

- `Ez nem csupán egy eszköz, hanem egy szemléletmód.` (§9 magyarul)
- `Merüljünk el a részletekben.` (`Let's dive in`)
- `A nap végén ami igazán számít...` (`At the end of the day`)
- `Ez egy olyan dolog, ami...` (`This is something that...`)
- `Legyünk őszinték.` önálló nyitómondatként (§33)

### Alárendelő láncok

Az AI magyarul hosszú, többszörösen alárendelt mondatokat gyárt, amelyekben a főige a végére
csúszik. Törd fel őket. Magyar szórend: ami új, az az ige elé kerül, és a hangsúly oda esik.

- Rossz: `A monitorozás, amely naponta egyszer fut le, és amelynek eredményeit a rendszer egy
  külön táblában tárolja, riasztást küld, amennyiben a konfiguráció megváltozik.`
- Jó: `A monitorozás naponta egyszer fut. Ha a konfiguráció közben megváltozik, riasztást küld.
  Az eredményt külön táblában tároljuk.`

### Tegezés és magázás

Egy szövegen belül egyféle. Az „Ön” és a „te” keveredése egy bekezdésen belül az egyik
legfeltűnőbb gépi jel magyarul. Ha nincs megadva, a ZeroHook-hangnem tegező.

## Amit magyarul **ne** jelölj hibának

- A hosszabb mondat magyarul természetesebb, mint angolul. A cél a változatosság, nem a rövidítés.
- A szenvedő értelmű `-ható/-hető` képző rendes magyar alak, nem passzív hiba.
- A birtokos szerkezetek halmozása néha egyszerűen szakmai nyelv (`a tanúsítvány lejáratának
  dátuma`), csak akkor bontsd, ha három tagnál hosszabb.
- A gondolatjel és a „ ” idézőjel, ahogy fent.
- **Kódérték idézőjelben.** A „ ” a szövegé, nem az azonosítóé. A `"Pending"`, a `"queued"`
  és a `"delayed"` állapotnév, egyenes idézőjellel vagy backtickkel helyes; a „Pending” hibás
  lenne. A checker ezért csak azt jelzi, ami magyar szövegnek olvasódik: több szóból áll, vagy
  van benne magyar ékezet.
- Az idegen szakszó, ha nincs bevett magyar megfelelője. A `DMARC-rekord` marad DMARC-rekord;
  ne fordítsd le, és ne írd körül.

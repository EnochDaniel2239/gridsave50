import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent
OUT_DIR = BASE_DIR / "dist"

# Replace these placeholder URLs with your approved affiliate/quote links
SITE_BASE_URL = "https://gridsave50.pages.dev"
QUOTE_URL = "https://example.com/get-solar-quotes"
BATTERY_URL = "https://example.com/backup-batteries"


def render_page(title: str, description: str, heading: str, subtitle: str, body_html: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{description}" />
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen antialiased">
  <header class="border-b border-slate-800 bg-slate-900/70 backdrop-blur sticky top-0 z-10">
    <div class="max-w-4xl mx-auto px-4 py-3.5 flex items-center justify-between">
      <a href="/index.html" class="font-bold text-lg tracking-tight text-emerald-400">
        GridSave<span class="text-slate-100">50</span>
      </a>
      <a href="/index.html" class="text-xs sm:text-sm text-slate-300 hover:text-white transition">
        All 50 States &rarr;
      </a>
    </div>
  </header>

  <main class="max-w-4xl mx-auto px-4 py-8">
    <div class="mb-6">
      <h1 class="text-2xl sm:text-3xl font-bold text-white">{heading}</h1>
      <p class="text-slate-400 mt-1.5 text-sm sm:text-base">{subtitle}</p>
    </div>

    {body_html}

    <footer class="mt-12 pt-6 border-t border-slate-800 text-xs text-slate-500 space-y-2">
      <p>
        <strong>Disclaimer:</strong> Estimates are illustrative planning models based on state average utility rates,
        peak sun hours, system sizing, and assumed utility bill inflation. Actual quotes, roof shading, net metering
        rules, and incentives vary by utility provider and property.
      </p>
      <p>
        <strong>Affiliate Disclosure:</strong> This site may earn a commission or referral fee if you click partner
        quote or equipment links and complete a qualifying action, at no extra cost to you.
      </p>
    </footer>
  </main>
</body>
</html>
"""


def build_state_page(state_obj: dict, all_states: list[dict]) -> str:
    state_name = state_obj["state"]
    rate = state_obj["rate"]
    sun_hours = state_obj["sun_hours"]
    slug = state_obj["slug"]

    other_links = "".join(
        f'<a href="/{s["slug"]}-solar-calculator.html" '
        f'class="px-2.5 py-1 rounded bg-slate-900 border border-slate-800 hover:border-emerald-500/60 text-xs text-slate-300">'
        f'{s["code"]}</a>'
        for s in all_states
    )

    body = f"""
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
      <section class="lg:col-span-6 bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-5">
        <div class="grid grid-cols-2 gap-3 text-sm">
          <div class="bg-slate-950 border border-slate-800 rounded-lg p-3">
            <div class="text-slate-400 text-xs">Avg. {state_name} Rate</div>
            <div id="rateDisplay" class="text-lg font-semibold text-emerald-400 mt-0.5">${rate:.3f}/kWh</div>
          </div>
          <div class="bg-slate-950 border border-slate-800 rounded-lg p-3">
            <div class="text-slate-400 text-xs">Peak Sun Hours</div>
            <div id="sunDisplay" class="text-lg font-semibold text-amber-400 mt-0.5">{sun_hours:.1f} hrs/day</div>
          </div>
        </div>

        <div>
          <label for="billInput" class="block text-sm font-medium text-slate-200 mb-1.5">
            Monthly Electric Bill ($)
          </label>
          <input id="billInput" type="number" min="30" max="2000" step="10" value="180"
            class="w-full rounded-lg bg-slate-950 border border-slate-700 px-3.5 py-2.5 text-white focus:outline-none focus:border-emerald-400" />
          <input id="billSlider" type="range" min="40" max="1000" step="10" value="180"
            class="w-full mt-2 accent-emerald-400" />
        </div>

        <div>
          <label for="offsetSelect" class="block text-sm font-medium text-slate-200 mb-1.5">
            Target Bill Offset (%)
          </label>
          <select id="offsetSelect"
            class="w-full rounded-lg bg-slate-950 border border-slate-700 px-3.5 py-2.5 text-white focus:outline-none focus:border-emerald-400">
            <option value="0.5">50% Offset (Starter / Shading)</option>
            <option value="0.8" selected>80% Offset (Typical System)</option>
            <option value="1.0">100% Offset (Full Bill Target)</option>
          </select>
        </div>

        <div>
          <label for="inflationInput" class="block text-sm font-medium text-slate-200 mb-1.5">
            Assumed Annual Utility Rate Increase (%)
          </label>
          <input id="inflationInput" type="number" min="0" max="15" step="0.5" value="3.5"
            class="w-full rounded-lg bg-slate-950 border border-slate-700 px-3.5 py-2.5 text-white focus:outline-none focus:border-emerald-400" />
        </div>
      </section>

      <section class="lg:col-span-6 bg-slate-900 border border-slate-800 rounded-xl p-5 flex flex-col justify-between space-y-5">
        <div class="space-y-4">
          <div class="text-xs uppercase tracking-wider text-slate-400 font-semibold">Estimated Results</div>

          <div class="grid grid-cols-2 gap-3">
            <div class="bg-slate-950 border border-slate-800 rounded-lg p-3.5">
              <div class="text-xs text-slate-400">Est. System Size</div>
              <div id="sysSize" class="text-xl font-bold text-white mt-1">-- kW</div>
            </div>
            <div class="bg-slate-950 border border-slate-800 rounded-lg p-3.5">
              <div class="text-xs text-slate-400">Year 1 Savings</div>
              <div id="yr1Savings" class="text-xl font-bold text-emerald-400 mt-1">$--</div>
            </div>
            <div class="bg-slate-950 border border-slate-800 rounded-lg p-3.5">
              <div class="text-xs text-slate-400">10-Year Savings</div>
              <div id="yr10Savings" class="text-xl font-bold text-emerald-300 mt-1">$--</div>
            </div>
            <div class="bg-slate-950 border border-slate-800 rounded-lg p-3.5">
              <div class="text-xs text-slate-400">25-Year Savings</div>
              <div id="yr25Savings" class="text-xl font-bold text-emerald-400 mt-1">$--</div>
            </div>
          </div>

          <div class="bg-slate-950/90 border border-slate-800 rounded-lg p-3.5 text-xs text-slate-300 flex items-center justify-between">
            <span>Est. Gross System Cost (~$2.85/W):</span>
            <span id="grossCost" class="font-semibold text-white">$--</span>
          </div>
        </div>

        <div class="space-y-2.5 pt-2">
          <a href="{QUOTE_URL}" target="_blank" rel="noopener noreferrer sponsored"
            class="block w-full text-center bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-semibold py-3 px-4 rounded-lg transition">
            Compare {state_name} Solar Quotes &rarr;
          </a>
          <a href="{BATTERY_URL}" target="_blank" rel="noopener noreferrer sponsored"
            class="block w-full text-center bg-slate-800 hover:bg-slate-700 text-slate-100 font-medium py-2.5 px-4 rounded-lg transition text-sm">
            Explore Home Backup Batteries & Power Stations
          </a>
        </div>
      </section>
    </div>

    <section class="mt-8 bg-slate-900/60 border border-slate-800 rounded-xl p-5">
      <h2 class="text-base font-semibold text-white mb-2">How {state_name} Solar Math Works Here</h2>
      <p class="text-sm text-slate-400 leading-relaxed">
        With a baseline electricity rate of <strong class="text-slate-200">${rate:.3f}/kWh</strong> and roughly
        <strong class="text-slate-200">{sun_hours:.1f} peak sun hours/day</strong> in {state_name}, a higher monthly
        bill requires a larger solar array to offset your target percentage of usage. Multi-year savings accumulate as
        annual utility rates adjust by your chosen inflation rate.
      </p>
      <div class="mt-4">
        <div class="text-xs text-slate-400 mb-2">Jump to another state:</div>
        <div class="flex flex-wrap gap-1.5">{other_links}</div>
      </div>
    </section>

    <script>
      const RATE = {rate};
      const SUN_HOURS = {sun_hours};
      const DERATE = 0.80; // system performance derate factor
      const COST_PER_WATT = 2.85;

      const billInput = document.getElementById("billInput");
      const billSlider = document.getElementById("billSlider");
      const offsetSelect = document.getElementById("offsetSelect");
      const inflationInput = document.getElementById("inflationInput");

      function fmtMoney(num) {{
        return "$" + Math.round(num).toLocaleString("en-US");
      }}

      function calculate() {{
        const bill = Math.max(0, parseFloat(billInput.value) || 0);
        const offset = parseFloat(offsetSelect.value) || 0.8;
        const growth = (parseFloat(inflationInput.value) || 0) / 100;

        const targetMonthlySavings = bill * offset;
        const annualKwhTarget = (targetMonthlySavings / RATE) * 12;
        const systemKw = Math.max(1, annualKwhTarget / (SUN_HOURS * 365 * DERATE));
        const grossSystemCost = systemKw * 1000 * COST_PER_WATT;

        let cum1 = 0, cum10 = 0, cum25 = 0;
        for (let year = 1; year <= 25; year++) {{
          const yrSavings = targetMonthlySavings * 12 * Math.pow(1 + growth, year - 1);
          if (year === 1) cum1 = yrSavings;
          if (year <= 10) cum10 += yrSavings;
          cum25 += yrSavings;
        }}

        document.getElementById("sysSize").textContent = systemKw.toFixed(1) + " kW";
        document.getElementById("yr1Savings").textContent = fmtMoney(cum1);
        document.getElementById("yr10Savings").textContent = fmtMoney(cum10);
        document.getElementById("yr25Savings").textContent = fmtMoney(cum25);
        document.getElementById("grossCost").textContent = fmtMoney(grossSystemCost);
      }}

      billSlider.addEventListener("input", () => {{
        billInput.value = billSlider.value;
        calculate();
      }});
      billInput.addEventListener("input", () => {{
        billSlider.value = billInput.value;
        calculate();
      }});
      offsetSelect.addEventListener("change", calculate);
      inflationInput.addEventListener("input", calculate);

      calculate();
    </script>
    """

    return render_page(
        title=f"{state_name} Solar Savings & Bill Offset Calculator | GridSave50",
        description=f"Estimate {state_name} solar panel system size, 1-year, 10-year, and 25-year electricity savings using ${rate:.3f}/kWh and {sun_hours:.1f} peak sun hours.",
        heading=f"{state_name} Solar Savings Calculator",
        subtitle=f"Estimate solar system size and multi-year electric bill savings in {state_name} ({state_obj['code']}).",
        body_html=body,
    )


def build_index_page(states: list[dict]) -> str:
    cards = "".join(
        f"""
        <a href="/{s['slug']}-solar-calculator.html"
           class="block bg-slate-900 hover:bg-slate-800/90 border border-slate-800 hover:border-emerald-500/60 rounded-xl p-4 transition">
          <div class="flex items-center justify-between">
            <span class="font-semibold text-white">{s['state']}</span>
            <span class="text-xs px-2 py-0.5 rounded bg-slate-950 text-emerald-400 border border-slate-800">{s['code']}</span>
          </div>
          <div class="mt-2 text-xs text-slate-400 flex justify-between">
            <span>Rate: <strong class="text-slate-200">${s['rate']:.3f}/kWh</strong></span>
            <span>Sun: <strong class="text-slate-200">{s['sun_hours']:.1f}h/d</strong></span>
          </div>
        </a>
        """
        for s in states
    )

    body = f"""
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3.5">
      {cards}
    </div>
    """

    return render_page(
        title="50-State Solar & Electric Bill Savings Calculators | GridSave50",
        description="Compare electricity rates, peak sun hours, system sizes, and estimated solar savings across all 50 US states.",
        heading="50-State Solar Savings Calculators",
        subtitle="Select a state below to run a customized solar bill-offset and multi-year savings estimate.",
        body_html=body,
    )


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(BASE_DIR / "data.json", "r", encoding="utf-8") as f:
        states = json.load(f)

    (OUT_DIR / "index.html").write_text(build_index_page(states), encoding="utf-8")

    urls = [f"{SITE_BASE_URL}/index.html"]
    for s in states:
        filename = f"{s['slug']}-solar-calculator.html"
        (OUT_DIR / filename).write_text(build_state_page(s, states), encoding="utf-8")
        urls.append(f"{SITE_BASE_URL}/{filename}")

    sitemap_entries = "\n".join(f"  <url><loc>{u}</loc></url>" for u in urls)
    sitemap_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{sitemap_entries}
</urlset>
"""
    (OUT_DIR / "sitemap.xml").write_text(sitemap_xml, encoding="utf-8")
    (OUT_DIR / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {SITE_BASE_URL}/sitemap.xml\n",
        encoding="utf-8",
    )
    print(f"Generated {len(states)} state pages + index.html + sitemap.xml in '{OUT_DIR}'.")


if __name__ == "__main__":
    main()
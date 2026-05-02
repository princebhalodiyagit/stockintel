import yfinance as yf
import requests
import xml.etree.ElementTree as ET
import json, os, time
from datetime import datetime

os.makedirs("data/financials", exist_ok=True)
os.makedirs("data/news", exist_ok=True)
os.makedirs("data/directors", exist_ok=True)

COMPANIES = [
  {
    "name": "20 Microns Limited",
    "ticker": "20MICRONS",
    "yf": "20MICRONS.NS"
  },
  {
    "name": "21st Century Management Services Limited",
    "ticker": "21STCENMGM",
    "yf": "21STCENMGM.NS"
  },
  {
    "name": "360 ONE WAM LIMITED",
    "ticker": "360ONE",
    "yf": "360ONE.NS"
  },
  {
    "name": "3B Blackbio Dx Limited",
    "ticker": "3BBLACKBIO",
    "yf": "3BBLACKBIO.NS"
  },
  {
    "name": "3i Infotech Limited",
    "ticker": "3IINFOLTD",
    "yf": "3IINFOLTD.NS"
  },
  {
    "name": "3M India Limited",
    "ticker": "3MINDIA",
    "yf": "3MINDIA.NS"
  },
  {
    "name": "3P Land Holdings Limited",
    "ticker": "3PLAND",
    "yf": "3PLAND.NS"
  },
  {
    "name": "5Paisa Capital Limited",
    "ticker": "5PAISA",
    "yf": "5PAISA.NS"
  },
  {
    "name": "63 moons technologies limited",
    "ticker": "63MOONS",
    "yf": "63MOONS.NS"
  },
  {
    "name": "AAA Technologies Limited",
    "ticker": "AAATECH",
    "yf": "AAATECH.NS"
  },
  {
    "name": "Aadhar Housing Finance Limited",
    "ticker": "AADHARHFC",
    "yf": "AADHARHFC.NS"
  },
  {
    "name": "Aarnav Fashions Limited",
    "ticker": "AARNAV",
    "yf": "AARNAV.NS"
  },
  {
    "name": "Aaron Industries Limited",
    "ticker": "AARON",
    "yf": "AARON.NS"
  },
  {
    "name": "Aartech Solonics Limited",
    "ticker": "AARTECH",
    "yf": "AARTECH.NS"
  },
  {
    "name": "Aarti Drugs Limited",
    "ticker": "AARTIDRUGS",
    "yf": "AARTIDRUGS.NS"
  },
  {
    "name": "Aarti Industries Limited",
    "ticker": "AARTIIND",
    "yf": "AARTIIND.NS"
  },
  {
    "name": "Aarti Pharmalabs Limited",
    "ticker": "AARTIPHARM",
    "yf": "AARTIPHARM.NS"
  },
  {
    "name": "Aarti Surfactants Limited",
    "ticker": "AARTISURF",
    "yf": "AARTISURF.NS"
  },
  {
    "name": "Aarvi Encon Limited",
    "ticker": "AARVI",
    "yf": "AARVI.NS"
  },
  {
    "name": "Aavas Financiers Limited",
    "ticker": "AAVAS",
    "yf": "AAVAS.NS"
  },
  {
    "name": "Abans Enterprises Limited",
    "ticker": "ABANSENT",
    "yf": "ABANSENT.NS"
  },
  {
    "name": "ABB India Limited",
    "ticker": "ABB",
    "yf": "ABB.NS"
  },
  {
    "name": "Abbott India Limited",
    "ticker": "ABBOTINDIA",
    "yf": "ABBOTINDIA.NS"
  },
  {
    "name": "Aditya Birla Capital Limited",
    "ticker": "ABCAPITAL",
    "yf": "ABCAPITAL.NS"
  },
  {
    "name": "A B Cotspin India Limited",
    "ticker": "ABCOTS",
    "yf": "ABCOTS.NS"
  },
  {
    "name": "Allied Blenders and Distillers Limited",
    "ticker": "ABDL",
    "yf": "ABDL.NS"
  },
  {
    "name": "Aditya Birla Fashion and Retail Limited",
    "ticker": "ABFRL",
    "yf": "ABFRL.NS"
  },
  {
    "name": "A B Infrabuild Limited",
    "ticker": "ABINFRA",
    "yf": "ABINFRA.NS"
  },
  {
    "name": "Aditya Birla Lifestyle Brands Limited",
    "ticker": "ABLBL",
    "yf": "ABLBL.NS"
  },
  {
    "name": "ABM Knowledgeware Limited",
    "ticker": "ABMKNO",
    "yf": "ABMKNO.NS"
  },
  {
    "name": "Aditya Birla Real Estate Limited",
    "ticker": "ABREL",
    "yf": "ABREL.NS"
  },
  {
    "name": "Aditya Birla Sun Life AMC Limited",
    "ticker": "ABSLAMC",
    "yf": "ABSLAMC.NS"
  },
  {
    "name": "ACC Limited",
    "ticker": "ACC",
    "yf": "ACC.NS"
  },
  {
    "name": "Accelya Solutions India Limited",
    "ticker": "ACCELYA",
    "yf": "ACCELYA.NS"
  },
  {
    "name": "Action Construction Equipment Limited",
    "ticker": "ACE",
    "yf": "ACE.NS"
  },
  {
    "name": "Ace Integrated Solutions Limited",
    "ticker": "ACEINTEG",
    "yf": "ACEINTEG.NS"
  },
  {
    "name": "Archean Chemical Industries Limited",
    "ticker": "ACI",
    "yf": "ACI.NS"
  },
  {
    "name": "Andhra Cements Limited",
    "ticker": "ACL",
    "yf": "ACL.NS"
  },
  {
    "name": "Acme Solar Holdings Limited",
    "ticker": "ACMESOLAR",
    "yf": "ACMESOLAR.NS"
  },
  {
    "name": "ACS Technologies Limited",
    "ticker": "ACSTECH",
    "yf": "ACSTECH.NS"
  },
  {
    "name": "Acutaas Chemicals Limited",
    "ticker": "ACUTAAS",
    "yf": "ACUTAAS.NS"
  },
  {
    "name": "Adani Energy Solutions Limited",
    "ticker": "ADANIENSOL",
    "yf": "ADANIENSOL.NS"
  },
  {
    "name": "Adani Enterprises Limited",
    "ticker": "ADANIENT",
    "yf": "ADANIENT.NS"
  },
  {
    "name": "Adani Green Energy Limited",
    "ticker": "ADANIGREEN",
    "yf": "ADANIGREEN.NS"
  },
  {
    "name": "Adani Ports and Special Economic Zone Limited",
    "ticker": "ADANIPORTS",
    "yf": "ADANIPORTS.NS"
  },
  {
    "name": "Adani Power Limited",
    "ticker": "ADANIPOWER",
    "yf": "ADANIPOWER.NS"
  },
  {
    "name": "ADF Foods Limited",
    "ticker": "ADFFOODS",
    "yf": "ADFFOODS.NS"
  },
  {
    "name": "Archidply Decor Limited",
    "ticker": "ADL",
    "yf": "ADL.NS"
  },
  {
    "name": "Ador Welding Limited",
    "ticker": "ADOR",
    "yf": "ADOR.NS"
  },
  {
    "name": "Adroit Infotech Limited",
    "ticker": "ADROITINFO",
    "yf": "ADROITINFO.NS"
  },
  {
    "name": "Allied Digital Services Limited",
    "ticker": "ADSL",
    "yf": "ADSL.NS"
  },
  {
    "name": "Advait Energy Transitions Limited",
    "ticker": "ADVAIT",
    "yf": "ADVAIT.NS"
  },
  {
    "name": "Advance Agrolife Limited",
    "ticker": "ADVANCE",
    "yf": "ADVANCE.NS"
  },
  {
    "name": "Advani Hotels & Resorts (India) Limited",
    "ticker": "ADVANIHOTR",
    "yf": "ADVANIHOTR.NS"
  },
  {
    "name": "Advent Hotels International Limited",
    "ticker": "ADVENTHTL",
    "yf": "ADVENTHTL.NS"
  },
  {
    "name": "Advanced Enzyme Technologies Limited",
    "ticker": "ADVENZYMES",
    "yf": "ADVENZYMES.NS"
  },
  {
    "name": "Aegis Logistics Limited",
    "ticker": "AEGISLOG",
    "yf": "AEGISLOG.NS"
  },
  {
    "name": "Aegis Vopak Terminals Limited",
    "ticker": "AEGISVOPAK",
    "yf": "AEGISVOPAK.NS"
  },
  {
    "name": "Aequs Limited",
    "ticker": "AEQUS",
    "yf": "AEQUS.NS"
  },
  {
    "name": "Aeroflex Enterprises Limited",
    "ticker": "AEROENTER",
    "yf": "AEROENTER.NS"
  },
  {
    "name": "Aeroflex Industries Limited",
    "ticker": "AEROFLEX",
    "yf": "AEROFLEX.NS"
  },
  {
    "name": "Aeroflex Neu Limited",
    "ticker": "AERONEU",
    "yf": "AERONEU.NS"
  },
  {
    "name": "Aether Industries Limited",
    "ticker": "AETHER",
    "yf": "AETHER.NS"
  },
  {
    "name": "Afcons Infrastructure Limited",
    "ticker": "AFCONS",
    "yf": "AFCONS.NS"
  },
  {
    "name": "Affle 3i Limited",
    "ticker": "AFFLE",
    "yf": "AFFLE.NS"
  },
  {
    "name": "Abans Financial Services Limited",
    "ticker": "AFSL",
    "yf": "AFSL.NS"
  },
  {
    "name": "Agarwal Industrial Corporation Limited",
    "ticker": "AGARIND",
    "yf": "AGARIND.NS"
  },
  {
    "name": "Dr. Agarwal's Health Care Limited",
    "ticker": "AGARWALEYE",
    "yf": "AGARWALEYE.NS"
  },
  {
    "name": "AGI Greenpac Limited",
    "ticker": "AGI",
    "yf": "AGI.NS"
  },
  {
    "name": "Agi Infra Limited",
    "ticker": "AGIIL",
    "yf": "AGIIL.NS"
  },
  {
    "name": "Agri-Tech (India) Limited",
    "ticker": "AGRITECH",
    "yf": "AGRITECH.NS"
  },
  {
    "name": "Agro Phos India Limited",
    "ticker": "AGROPHOS",
    "yf": "AGROPHOS.NS"
  },
  {
    "name": "Anlon Healthcare Limited",
    "ticker": "AHCL",
    "yf": "AHCL.NS"
  },
  {
    "name": "Ahlada Engineers Limited",
    "ticker": "AHLADA",
    "yf": "AHLADA.NS"
  },
  {
    "name": "Asian Hotels (East) Limited",
    "ticker": "AHLEAST",
    "yf": "AHLEAST.NS"
  },
  {
    "name": "Ahluwalia Contracts (India) Limited",
    "ticker": "AHLUCONT",
    "yf": "AHLUCONT.NS"
  },
  {
    "name": "AIA Engineering Limited",
    "ticker": "AIAENG",
    "yf": "AIAENG.NS"
  },
  {
    "name": "Authum Investment & Infrastructure Limited",
    "ticker": "AIIL",
    "yf": "AIIL.NS"
  },
  {
    "name": "Airan Limited",
    "ticker": "AIRAN",
    "yf": "AIRAN.NS"
  },
  {
    "name": "Airo Lam limited",
    "ticker": "AIROLAM",
    "yf": "AIROLAM.NS"
  },
  {
    "name": "Ajanta Pharma Limited",
    "ticker": "AJANTPHARM",
    "yf": "AJANTPHARM.NS"
  },
  {
    "name": "Ajax Engineering Limited",
    "ticker": "AJAXENGG",
    "yf": "AJAXENGG.NS"
  },
  {
    "name": "Ajmera Realty & Infra India Limited",
    "ticker": "AJMERA",
    "yf": "AJMERA.NS"
  },
  {
    "name": "Ajooni Biotech Limited",
    "ticker": "AJOONI",
    "yf": "AJOONI.NS"
  },
  {
    "name": "Akash Infra-Projects Limited",
    "ticker": "AKASH",
    "yf": "AKASH.NS"
  },
  {
    "name": "AK Capital Services Limited",
    "ticker": "AKCAPIT",
    "yf": "AKCAPIT.NS"
  },
  {
    "name": "Akg Exim Limited",
    "ticker": "AKG",
    "yf": "AKG.NS"
  },
  {
    "name": "AKI India Limited",
    "ticker": "AKI",
    "yf": "AKI.NS"
  },
  {
    "name": "Akshar Spintex Limited",
    "ticker": "AKSHAR",
    "yf": "AKSHAR.NS"
  },
  {
    "name": "AksharChem India Limited",
    "ticker": "AKSHARCHEM",
    "yf": "AKSHARCHEM.NS"
  },
  {
    "name": "Akums Drugs and Pharmaceuticals Limited",
    "ticker": "AKUMS",
    "yf": "AKUMS.NS"
  },
  {
    "name": "Alankit Limited",
    "ticker": "ALANKIT",
    "yf": "ALANKIT.NS"
  },
  {
    "name": "Albert David Limited",
    "ticker": "ALBERTDAVD",
    "yf": "ALBERTDAVD.NS"
  },
  {
    "name": "Alembic Limited",
    "ticker": "ALEMBICLTD",
    "yf": "ALEMBICLTD.NS"
  },
  {
    "name": "Algoquant Fintech Limited",
    "ticker": "ALGOQUANT",
    "yf": "ALGOQUANT.NS"
  },
  {
    "name": "Alicon Castalloy Limited",
    "ticker": "ALICON",
    "yf": "ALICON.NS"
  },
  {
    "name": "Alivus Life Sciences Limited",
    "ticker": "ALIVUS",
    "yf": "ALIVUS.NS"
  },
  {
    "name": "Alkali Metals Limited",
    "ticker": "ALKALI",
    "yf": "ALKALI.NS"
  },
  {
    "name": "Alkem Laboratories Limited",
    "ticker": "ALKEM",
    "yf": "ALKEM.NS"
  },
  {
    "name": "Alkyl Amines Chemicals Limited",
    "ticker": "ALKYLAMINE",
    "yf": "ALKYLAMINE.NS"
  },
  {
    "name": "Allcargo Logistics Limited",
    "ticker": "ALLCARGO",
    "yf": "ALLCARGO.NS"
  },
  {
    "name": "Alldigi Tech Limited",
    "ticker": "ALLDIGI",
    "yf": "ALLDIGI.NS"
  },
  {
    "name": "All Time Plastics Limited",
    "ticker": "ALLTIME",
    "yf": "ALLTIME.NS"
  },
  {
    "name": "Almondz Global Securities Limited",
    "ticker": "ALMONDZ",
    "yf": "ALMONDZ.NS"
  },
  {
    "name": "Alok Industries Limited",
    "ticker": "ALOKINDS",
    "yf": "ALOKINDS.NS"
  },
  {
    "name": "Alpa Laboratories Limited",
    "ticker": "ALPA",
    "yf": "ALPA.NS"
  },
  {
    "name": "Alphageo (India) Limited",
    "ticker": "ALPHAGEO",
    "yf": "ALPHAGEO.NS"
  },
  {
    "name": "Amagi Media Labs Limited",
    "ticker": "AMAGI",
    "yf": "AMAGI.NS"
  },
  {
    "name": "Amanta Healthcare Limited",
    "ticker": "AMANTA",
    "yf": "AMANTA.NS"
  },
  {
    "name": "Ambalal Sarabhai Enterprises Limited",
    "ticker": "AMBALALSA",
    "yf": "AMBALALSA.NS"
  },
  {
    "name": "Amber Enterprises India Limited",
    "ticker": "AMBER",
    "yf": "AMBER.NS"
  },
  {
    "name": "Ambica Agarbathies & Aroma industries Limited",
    "ticker": "AMBICAAGAR",
    "yf": "AMBICAAGAR.NS"
  },
  {
    "name": "Ambika Cotton Mills Limited",
    "ticker": "AMBIKCO",
    "yf": "AMBIKCO.NS"
  },
  {
    "name": "Ambuja Cements Limited",
    "ticker": "AMBUJACEM",
    "yf": "AMBUJACEM.NS"
  },
  {
    "name": "AMD Industries Limited",
    "ticker": "AMDIND",
    "yf": "AMDIND.NS"
  },
  {
    "name": "Amir Chand Jagdish Kumar (Exports) Limited",
    "ticker": "AMIRCHAND",
    "yf": "AMIRCHAND.NS"
  },
  {
    "name": "Amj Land Holdings Limited",
    "ticker": "AMJLAND",
    "yf": "AMJLAND.NS"
  },
  {
    "name": "Amines & Plasticizers Limited",
    "ticker": "AMNPLST",
    "yf": "AMNPLST.NS"
  },
  {
    "name": "Amrutanjan Health Care Limited",
    "ticker": "AMRUTANJAN",
    "yf": "AMRUTANJAN.NS"
  },
  {
    "name": "Anand Rathi Wealth Limited",
    "ticker": "ANANDRATHI",
    "yf": "ANANDRATHI.NS"
  },
  {
    "name": "Anant Raj Limited",
    "ticker": "ANANTRAJ",
    "yf": "ANANTRAJ.NS"
  },
  {
    "name": "ANDHRA PAPER LIMITED",
    "ticker": "ANDHRAPAP",
    "yf": "ANDHRAPAP.NS"
  },
  {
    "name": "The Andhra Sugars Limited",
    "ticker": "ANDHRSUGAR",
    "yf": "ANDHRSUGAR.NS"
  },
  {
    "name": "Angel One Limited",
    "ticker": "ANGELONE",
    "yf": "ANGELONE.NS"
  },
  {
    "name": "Anmol India Limited",
    "ticker": "ANMOL",
    "yf": "ANMOL.NS"
  },
  {
    "name": "Antelopus Selan Energy Limited",
    "ticker": "ANTELOPUS",
    "yf": "ANTELOPUS.NS"
  },
  {
    "name": "Antarctica Limited",
    "ticker": "ANTGRAPHIC",
    "yf": "ANTGRAPHIC.NS"
  },
  {
    "name": "Anthem Biosciences Limited",
    "ticker": "ANTHEM",
    "yf": "ANTHEM.NS"
  },
  {
    "name": "Anuh Pharma Limited",
    "ticker": "ANUHPHR",
    "yf": "ANUHPHR.NS"
  },
  {
    "name": "The Anup Engineering Limited",
    "ticker": "ANUP",
    "yf": "ANUP.NS"
  },
  {
    "name": "Anupam Rasayan India Limited",
    "ticker": "ANURAS",
    "yf": "ANURAS.NS"
  },
  {
    "name": "Apar Industries Limited",
    "ticker": "APARINDS",
    "yf": "APARINDS.NS"
  },
  {
    "name": "Anjani Portland Cement Limited",
    "ticker": "APCL",
    "yf": "APCL.NS"
  },
  {
    "name": "Apcotex Industries Limited",
    "ticker": "APCOTEXIND",
    "yf": "APCOTEXIND.NS"
  },
  {
    "name": "Apex Frozen Foods Limited",
    "ticker": "APEX",
    "yf": "APEX.NS"
  },
  {
    "name": "APL Apollo Tubes Limited",
    "ticker": "APLAPOLLO",
    "yf": "APLAPOLLO.NS"
  },
  {
    "name": "Alembic Pharmaceuticals Limited",
    "ticker": "APLLTD",
    "yf": "APLLTD.NS"
  },
  {
    "name": "Apollo Micro Systems Limited",
    "ticker": "APOLLO",
    "yf": "APOLLO.NS"
  },
  {
    "name": "Apollo Hospitals Enterprise Limited",
    "ticker": "APOLLOHOSP",
    "yf": "APOLLOHOSP.NS"
  },
  {
    "name": "Apollo Pipes Limited",
    "ticker": "APOLLOPIPE",
    "yf": "APOLLOPIPE.NS"
  },
  {
    "name": "Apollo Tyres Limited",
    "ticker": "APOLLOTYRE",
    "yf": "APOLLOTYRE.NS"
  },
  {
    "name": "Apollo Sindoori Hotels Limited",
    "ticker": "APOLSINHOT",
    "yf": "APOLSINHOT.NS"
  },
  {
    "name": "Aptech Limited",
    "ticker": "APTECHT",
    "yf": "APTECHT.NS"
  },
  {
    "name": "Aptus Value Housing Finance India Limited",
    "ticker": "APTUS",
    "yf": "APTUS.NS"
  },
  {
    "name": "Aqylon Nexus Limited",
    "ticker": "AQYLON",
    "yf": "AQYLON.NS"
  },
  {
    "name": "Archidply Industries Limited",
    "ticker": "ARCHIDPLY",
    "yf": "ARCHIDPLY.NS"
  },
  {
    "name": "Archies Limited",
    "ticker": "ARCHIES",
    "yf": "ARCHIES.NS"
  },
  {
    "name": "Amara Raja Energy & Mobility Limited",
    "ticker": "ARE&M",
    "yf": "ARE&M.NS"
  },
  {
    "name": "Rajdarshan Industries Limited",
    "ticker": "ARENTERP",
    "yf": "ARENTERP.NS"
  },
  {
    "name": "Arfin India Limited",
    "ticker": "ARFIN",
    "yf": "ARFIN.NS"
  },
  {
    "name": "Aries Agro Limited",
    "ticker": "ARIES",
    "yf": "ARIES.NS"
  },
  {
    "name": "Arihant Foundations & Housing Limited",
    "ticker": "ARIHANT",
    "yf": "ARIHANT.NS"
  },
  {
    "name": "Arihant Capital Markets Limited",
    "ticker": "ARIHANTCAP",
    "yf": "ARIHANTCAP.NS"
  },
  {
    "name": "Arihant Superstructures Limited",
    "ticker": "ARIHANTSUP",
    "yf": "ARIHANTSUP.NS"
  },
  {
    "name": "Arisinfra Solutions Limited",
    "ticker": "ARIS",
    "yf": "ARIS.NS"
  },
  {
    "name": "Arkade Developers Limited",
    "ticker": "ARKADE",
    "yf": "ARKADE.NS"
  },
  {
    "name": "Arman Financial Services Limited",
    "ticker": "ARMANFIN",
    "yf": "ARMANFIN.NS"
  },
  {
    "name": "Aro Granite Industries Limited",
    "ticker": "AROGRANITE",
    "yf": "AROGRANITE.NS"
  },
  {
    "name": "Arrow Greentech Limited",
    "ticker": "ARROWGREEN",
    "yf": "ARROWGREEN.NS"
  },
  {
    "name": "Anand Rathi Share and Stock Brokers Limited",
    "ticker": "ARSSBL",
    "yf": "ARSSBL.NS"
  },
  {
    "name": "Artemis Medicare Services Limited",
    "ticker": "ARTEMISMED",
    "yf": "ARTEMISMED.NS"
  },
  {
    "name": "Arvee Laboratories (India) Limited",
    "ticker": "ARVEE",
    "yf": "ARVEE.NS"
  },
  {
    "name": "Arvind Limited",
    "ticker": "ARVIND",
    "yf": "ARVIND.NS"
  },
  {
    "name": "Arvind Fashions Limited",
    "ticker": "ARVINDFASN",
    "yf": "ARVINDFASN.NS"
  },
  {
    "name": "Arvind SmartSpaces Limited",
    "ticker": "ARVSMART",
    "yf": "ARVSMART.NS"
  },
  {
    "name": "Asahi India Glass Limited",
    "ticker": "ASAHIINDIA",
    "yf": "ASAHIINDIA.NS"
  },
  {
    "name": "Asahi Songwon Colors Limited",
    "ticker": "ASAHISONG",
    "yf": "ASAHISONG.NS"
  },
  {
    "name": "Automotive Stampings and Assemblies Limited",
    "ticker": "ASAL",
    "yf": "ASAL.NS"
  },
  {
    "name": "Associated Alcohols & Breweries Ltd.",
    "ticker": "ASALCBR",
    "yf": "ASALCBR.NS"
  },
  {
    "name": "Ashapura Minechem Limited",
    "ticker": "ASHAPURMIN",
    "yf": "ASHAPURMIN.NS"
  },
  {
    "name": "Ashiana Housing Limited",
    "ticker": "ASHIANA",
    "yf": "ASHIANA.NS"
  },
  {
    "name": "Ashika Credit Capital Limited",
    "ticker": "ASHIKA",
    "yf": "ASHIKA.NS"
  },
  {
    "name": "Ashima Limited",
    "ticker": "ASHIMASYN",
    "yf": "ASHIMASYN.NS"
  },
  {
    "name": "Ashoka Buildcon Limited",
    "ticker": "ASHOKA",
    "yf": "ASHOKA.NS"
  },
  {
    "name": "Ashoka Metcast Limited",
    "ticker": "ASHOKAMET",
    "yf": "ASHOKAMET.NS"
  },
  {
    "name": "Ashok Leyland Limited",
    "ticker": "ASHOKLEY",
    "yf": "ASHOKLEY.NS"
  },
  {
    "name": "Asian Energy Services Limited",
    "ticker": "ASIANENE",
    "yf": "ASIANENE.NS"
  },
  {
    "name": "Asian Hotels (North) Limited",
    "ticker": "ASIANHOTNR",
    "yf": "ASIANHOTNR.NS"
  },
  {
    "name": "Asian Paints Limited",
    "ticker": "ASIANPAINT",
    "yf": "ASIANPAINT.NS"
  },
  {
    "name": "Asian Granito India Limited",
    "ticker": "ASIANTILES",
    "yf": "ASIANTILES.NS"
  },
  {
    "name": "ASK Automotive Limited",
    "ticker": "ASKAUTOLTD",
    "yf": "ASKAUTOLTD.NS"
  },
  {
    "name": "Bartronics India Limited",
    "ticker": "ASMS",
    "yf": "ASMS.NS"
  },
  {
    "name": "Aspinwall and Company Limited",
    "ticker": "ASPINWALL",
    "yf": "ASPINWALL.NS"
  },
  {
    "name": "Asian Star Company Limited",
    "ticker": "ASTAR",
    "yf": "ASTAR.NS"
  },
  {
    "name": "Astec LifeSciences Limited",
    "ticker": "ASTEC",
    "yf": "ASTEC.NS"
  },
  {
    "name": "Aster DM Healthcare Limited",
    "ticker": "ASTERDM",
    "yf": "ASTERDM.NS"
  },
  {
    "name": "Astral Limited",
    "ticker": "ASTRAL",
    "yf": "ASTRAL.NS"
  },
  {
    "name": "Astra Microwave Products Limited",
    "ticker": "ASTRAMICRO",
    "yf": "ASTRAMICRO.NS"
  },
  {
    "name": "AstraZeneca Pharma India Limited",
    "ticker": "ASTRAZEN",
    "yf": "ASTRAZEN.NS"
  },
  {
    "name": "Atal Realtech Limited",
    "ticker": "ATALREAL",
    "yf": "ATALREAL.NS"
  },
  {
    "name": "Atam Valves Limited",
    "ticker": "ATAM",
    "yf": "ATAM.NS"
  },
  {
    "name": "Adani Total Gas Limited",
    "ticker": "ATGL",
    "yf": "ATGL.NS"
  },
  {
    "name": "Ather Energy Limited",
    "ticker": "ATHERENERG",
    "yf": "ATHERENERG.NS"
  },
  {
    "name": "Allcargo Terminals Limited",
    "ticker": "ATL",
    "yf": "ATL.NS"
  },
  {
    "name": "ATLANTAA LIMITED",
    "ticker": "ATLANTAA",
    "yf": "ATLANTAA.NS"
  },
  {
    "name": "Atlas Cycles (Haryana) Limited",
    "ticker": "ATLASCYCLE",
    "yf": "ATLASCYCLE.NS"
  },
  {
    "name": "Atul Limited",
    "ticker": "ATUL",
    "yf": "ATUL.NS"
  },
  {
    "name": "Atul Auto Limited",
    "ticker": "ATULAUTO",
    "yf": "ATULAUTO.NS"
  },
  {
    "name": "AU Small Finance Bank Limited",
    "ticker": "AUBANK",
    "yf": "AUBANK.NS"
  },
  {
    "name": "Auri Grow India Limited",
    "ticker": "AURIGROW",
    "yf": "AURIGROW.NS"
  },
  {
    "name": "Aurionpro Solutions Limited",
    "ticker": "AURIONPRO",
    "yf": "AURIONPRO.NS"
  },
  {
    "name": "Aurobindo Pharma Limited",
    "ticker": "AUROPHARMA",
    "yf": "AUROPHARMA.NS"
  },
  {
    "name": "Aurum PropTech Limited",
    "ticker": "AURUM",
    "yf": "AURUM.NS"
  },
  {
    "name": "Ausom Enterprise Limited",
    "ticker": "AUSOMENT",
    "yf": "AUSOMENT.NS"
  },
  {
    "name": "Automotive Axles Limited",
    "ticker": "AUTOAXLES",
    "yf": "AUTOAXLES.NS"
  },
  {
    "name": "Autoline Industries Limited",
    "ticker": "AUTOIND",
    "yf": "AUTOIND.NS"
  },
  {
    "name": "Available Finance Limited",
    "ticker": "AVAILFC",
    "yf": "AVAILFC.NS"
  },
  {
    "name": "Avalon Technologies Limited",
    "ticker": "AVALON",
    "yf": "AVALON.NS"
  },
  {
    "name": "Avantel Limited",
    "ticker": "AVANTEL",
    "yf": "AVANTEL.NS"
  },
  {
    "name": "Avanti Feeds Limited",
    "ticker": "AVANTIFEED",
    "yf": "AVANTIFEED.NS"
  },
  {
    "name": "AVG Logistics Limited",
    "ticker": "AVG",
    "yf": "AVG.NS"
  },
  {
    "name": "Aditya Vision Limited",
    "ticker": "AVL",
    "yf": "AVL.NS"
  },
  {
    "name": "Avonmore Capital & Management Services Limited",
    "ticker": "AVONMORE",
    "yf": "AVONMORE.NS"
  },
  {
    "name": "AVRO INDIA LIMITED",
    "ticker": "AVROIND",
    "yf": "AVROIND.NS"
  },
  {
    "name": "AVT Natural Products Limited",
    "ticker": "AVTNPL",
    "yf": "AVTNPL.NS"
  },
  {
    "name": "Awfis Space Solutions Limited",
    "ticker": "AWFIS",
    "yf": "AWFIS.NS"
  },
  {
    "name": "Antony Waste Handling Cell Limited",
    "ticker": "AWHCL",
    "yf": "AWHCL.NS"
  },
  {
    "name": "AWL Agri Business Limited",
    "ticker": "AWL",
    "yf": "AWL.NS"
  },
  {
    "name": "Axis Bank Limited",
    "ticker": "AXISBANK",
    "yf": "AXISBANK.NS"
  },
  {
    "name": "AXISCADES Technologies Limited",
    "ticker": "AXISCADES",
    "yf": "AXISCADES.NS"
  },
  {
    "name": "Axita Cotton Limited",
    "ticker": "AXITA",
    "yf": "AXITA.NS"
  },
  {
    "name": "Aye Finance Limited",
    "ticker": "AYE",
    "yf": "AYE.NS"
  },
  {
    "name": "AYM Syntex Limited",
    "ticker": "AYMSYNTEX",
    "yf": "AYMSYNTEX.NS"
  },
  {
    "name": "Azad Engineering Limited",
    "ticker": "AZAD",
    "yf": "AZAD.NS"
  },
  {
    "name": "B.A.G Films and Media Limited",
    "ticker": "BAGFILMS",
    "yf": "BAGFILMS.NS"
  },
  {
    "name": "Baid Finserv Limited",
    "ticker": "BAIDFIN",
    "yf": "BAIDFIN.NS"
  },
  {
    "name": "Bajaj Auto Limited",
    "ticker": "BAJAJ-AUTO",
    "yf": "BAJAJ-AUTO.NS"
  },
  {
    "name": "Bajaj Consumer Care Limited",
    "ticker": "BAJAJCON",
    "yf": "BAJAJCON.NS"
  },
  {
    "name": "Bajaj Electricals Limited",
    "ticker": "BAJAJELEC",
    "yf": "BAJAJELEC.NS"
  },
  {
    "name": "Bajaj Finserv Limited",
    "ticker": "BAJAJFINSV",
    "yf": "BAJAJFINSV.NS"
  },
  {
    "name": "Bajaj Healthcare Limited",
    "ticker": "BAJAJHCARE",
    "yf": "BAJAJHCARE.NS"
  },
  {
    "name": "Bajaj Housing Finance Limited",
    "ticker": "BAJAJHFL",
    "yf": "BAJAJHFL.NS"
  },
  {
    "name": "Bajaj Hindusthan Sugar Limited",
    "ticker": "BAJAJHIND",
    "yf": "BAJAJHIND.NS"
  },
  {
    "name": "Bajaj Holdings & Investment Limited",
    "ticker": "BAJAJHLDNG",
    "yf": "BAJAJHLDNG.NS"
  },
  {
    "name": "Indef Manufacturing Limited",
    "ticker": "BAJAJINDEF",
    "yf": "BAJAJINDEF.NS"
  },
  {
    "name": "Bajaj Steel Industries Limited",
    "ticker": "BAJAJST",
    "yf": "BAJAJST.NS"
  },
  {
    "name": "Bajel Projects Limited",
    "ticker": "BAJEL",
    "yf": "BAJEL.NS"
  },
  {
    "name": "Bajaj Finance Limited",
    "ticker": "BAJFINANCE",
    "yf": "BAJFINANCE.NS"
  },
  {
    "name": "Shree Tirupati Balajee Agro Trading Company Limited",
    "ticker": "BALAJEE",
    "yf": "BALAJEE.NS"
  },
  {
    "name": "Balaji Telefilms Limited",
    "ticker": "BALAJITELE",
    "yf": "BALAJITELE.NS"
  },
  {
    "name": "Balaji Amines Limited",
    "ticker": "BALAMINES",
    "yf": "BALAMINES.NS"
  },
  {
    "name": "Balkrishna Paper Mills Limited",
    "ticker": "BALKRISHNA",
    "yf": "BALKRISHNA.NS"
  },
  {
    "name": "Balkrishna Industries Limited",
    "ticker": "BALKRISIND",
    "yf": "BALKRISIND.NS"
  },
  {
    "name": "Balmer Lawrie & Company Limited",
    "ticker": "BALMLAWRIE",
    "yf": "BALMLAWRIE.NS"
  },
  {
    "name": "Bal Pharma Limited",
    "ticker": "BALPHARMA",
    "yf": "BALPHARMA.NS"
  },
  {
    "name": "Balrampur Chini Mills Limited",
    "ticker": "BALRAMCHIN",
    "yf": "BALRAMCHIN.NS"
  },
  {
    "name": "Balu Forge Industries Limited",
    "ticker": "BALUFORGE",
    "yf": "BALUFORGE.NS"
  },
  {
    "name": "Banaras Beads Limited",
    "ticker": "BANARBEADS",
    "yf": "BANARBEADS.NS"
  },
  {
    "name": "Bannari Amman Sugars Limited",
    "ticker": "BANARISUG",
    "yf": "BANARISUG.NS"
  },
  {
    "name": "Banco Products (I) Limited",
    "ticker": "BANCOINDIA",
    "yf": "BANCOINDIA.NS"
  },
  {
    "name": "Bandhan Bank Limited",
    "ticker": "BANDHANBNK",
    "yf": "BANDHANBNK.NS"
  },
  {
    "name": "Bang Overseas Limited",
    "ticker": "BANG",
    "yf": "BANG.NS"
  },
  {
    "name": "Bank of Baroda",
    "ticker": "BANKBARODA",
    "yf": "BANKBARODA.NS"
  },
  {
    "name": "Bank of India",
    "ticker": "BANKINDIA",
    "yf": "BANKINDIA.NS"
  },
  {
    "name": "Bansal Wire Industries Limited",
    "ticker": "BANSALWIRE",
    "yf": "BANSALWIRE.NS"
  },
  {
    "name": "Banswara Syntex Limited",
    "ticker": "BANSWRAS",
    "yf": "BANSWRAS.NS"
  },
  {
    "name": "BASF India Limited",
    "ticker": "BASF",
    "yf": "BASF.NS"
  },
  {
    "name": "Bannari Amman Spinning Mills Limited",
    "ticker": "BASML",
    "yf": "BASML.NS"
  },
  {
    "name": "Bata India Limited",
    "ticker": "BATAINDIA",
    "yf": "BATAINDIA.NS"
  },
  {
    "name": "Batliboi Limited",
    "ticker": "BATLIBOI",
    "yf": "BATLIBOI.NS"
  },
  {
    "name": "Bayer Cropscience Limited",
    "ticker": "BAYERCROP",
    "yf": "BAYERCROP.NS"
  },
  {
    "name": "Bharat Bijlee Limited",
    "ticker": "BBL",
    "yf": "BBL.NS"
  },
  {
    "name": "Black Box Limited",
    "ticker": "BBOX",
    "yf": "BBOX.NS"
  },
  {
    "name": "The Bombay Burmah Trading Corporation Limited",
    "ticker": "BBTC",
    "yf": "BBTC.NS"
  },
  {
    "name": "B&B Triplewall Containers Limited",
    "ticker": "BBTCL",
    "yf": "BBTCL.NS"
  },
  {
    "name": "Bcl Industries Limited",
    "ticker": "BCLIND",
    "yf": "BCLIND.NS"
  },
  {
    "name": "Brand Concepts Limited",
    "ticker": "BCONCEPTS",
    "yf": "BCONCEPTS.NS"
  },
  {
    "name": "BCPL Railway Infrastructure Limited",
    "ticker": "BCPL",
    "yf": "BCPL.NS"
  },
  {
    "name": "Bharat Dynamics Limited",
    "ticker": "BDL",
    "yf": "BDL.NS"
  },
  {
    "name": "Beardsell Limited",
    "ticker": "BEARDSELL",
    "yf": "BEARDSELL.NS"
  },
  {
    "name": "Mrs. Bectors Food Specialities Limited",
    "ticker": "BECTORFOOD",
    "yf": "BECTORFOOD.NS"
  },
  {
    "name": "Beekay Steel Industries Limited",
    "ticker": "BEEKAY",
    "yf": "BEEKAY.NS"
  },
  {
    "name": "Bharat Electronics Limited",
    "ticker": "BEL",
    "yf": "BEL.NS"
  },
  {
    "name": "Bella Casa Fashion & Retail Limited",
    "ticker": "BELLACASA",
    "yf": "BELLACASA.NS"
  },
  {
    "name": "Belrise Industries Limited",
    "ticker": "BELRISE",
    "yf": "BELRISE.NS"
  },
  {
    "name": "BEML Limited",
    "ticker": "BEML",
    "yf": "BEML.NS"
  },
  {
    "name": "Bengal & Assam Company Limited",
    "ticker": "BENGALASM",
    "yf": "BENGALASM.NS"
  },
  {
    "name": "Bhansali Engineering Polymers Limited",
    "ticker": "BEPL",
    "yf": "BEPL.NS"
  },
  {
    "name": "Berger Paints (I) Limited",
    "ticker": "BERGEPAINT",
    "yf": "BERGEPAINT.NS"
  },
  {
    "name": "Best Agrolife Limited",
    "ticker": "BESTAGRO",
    "yf": "BESTAGRO.NS"
  },
  {
    "name": "Beta Drugs Limited",
    "ticker": "BETA",
    "yf": "BETA.NS"
  },
  {
    "name": "BF Investment Limited",
    "ticker": "BFINVEST",
    "yf": "BFINVEST.NS"
  },
  {
    "name": "BF Utilities Limited",
    "ticker": "BFUTILITIE",
    "yf": "BFUTILITIE.NS"
  },
  {
    "name": "Bhagiradha Chemicals & Industries Limited",
    "ticker": "BHAGCHEM",
    "yf": "BHAGCHEM.NS"
  },
  {
    "name": "Bhageria Industries Limited",
    "ticker": "BHAGERIA",
    "yf": "BHAGERIA.NS"
  },
  {
    "name": "Bhandari Hosiery Exports Limited",
    "ticker": "BHANDARI",
    "yf": "BHANDARI.NS"
  },
  {
    "name": "Bharat Coking Coal Limited",
    "ticker": "BHARATCOAL",
    "yf": "BHARATCOAL.NS"
  },
  {
    "name": "Bharat Forge Limited",
    "ticker": "BHARATFORG",
    "yf": "BHARATFORG.NS"
  },
  {
    "name": "Bharat Gears Limited",
    "ticker": "BHARATGEAR",
    "yf": "BHARATGEAR.NS"
  },
  {
    "name": "Bharat Rasayan Limited",
    "ticker": "BHARATRAS",
    "yf": "BHARATRAS.NS"
  },
  {
    "name": "Bharat Seats Limited",
    "ticker": "BHARATSE",
    "yf": "BHARATSE.NS"
  },
  {
    "name": "Bharat Wire Ropes Limited",
    "ticker": "BHARATWIRE",
    "yf": "BHARATWIRE.NS"
  },
  {
    "name": "Bharti Airtel Limited",
    "ticker": "BHARTIARTL",
    "yf": "BHARTIARTL.NS"
  },
  {
    "name": "Bharti Hexacom Limited",
    "ticker": "BHARTIHEXA",
    "yf": "BHARTIHEXA.NS"
  },
  {
    "name": "Bharat Heavy Electricals Limited",
    "ticker": "BHEL",
    "yf": "BHEL.NS"
  },
  {
    "name": "Bilcare Limited",
    "ticker": "BI",
    "yf": "BI.NS"
  },
  {
    "name": "Bigbloc Construction Limited",
    "ticker": "BIGBLOC",
    "yf": "BIGBLOC.NS"
  },
  {
    "name": "Bikaji Foods International Limited",
    "ticker": "BIKAJI",
    "yf": "BIKAJI.NS"
  },
  {
    "name": "Bhartiya International Limited",
    "ticker": "BIL",
    "yf": "BIL.NS"
  },
  {
    "name": "Bimetal Bearings Limited",
    "ticker": "BIMETAL",
    "yf": "BIMETAL.NS"
  },
  {
    "name": "Biocon Limited",
    "ticker": "BIOCON",
    "yf": "BIOCON.NS"
  },
  {
    "name": "Biofil Chemicals & Pharmaceuticals Limited",
    "ticker": "BIOFILCHEM",
    "yf": "BIOFILCHEM.NS"
  },
  {
    "name": "Birla Corporation Limited",
    "ticker": "BIRLACORPN",
    "yf": "BIRLACORPN.NS"
  },
  {
    "name": "Aditya Birla Money Limited",
    "ticker": "BIRLAMONEY",
    "yf": "BIRLAMONEY.NS"
  },
  {
    "name": "BirlaNu Limited",
    "ticker": "BIRLANU",
    "yf": "BIRLANU.NS"
  },
  {
    "name": "Birla Precision Technologies Limited",
    "ticker": "BIRLAPREC",
    "yf": "BIRLAPREC.NS"
  },
  {
    "name": "BLACKBUCK LIMITED",
    "ticker": "BLACKBUCK",
    "yf": "BLACKBUCK.NS"
  },
  {
    "name": "Black Rose Inds. Limited",
    "ticker": "BLACKROSE",
    "yf": "BLACKROSE.NS"
  },
  {
    "name": "BEML Land Assets Limited",
    "ticker": "BLAL",
    "yf": "BLAL.NS"
  },
  {
    "name": "Balmer Lawrie Investments Limited",
    "ticker": "BLIL",
    "yf": "BLIL.NS"
  },
  {
    "name": "Bliss GVS Pharma Limited",
    "ticker": "BLISSGVS",
    "yf": "BLISSGVS.NS"
  },
  {
    "name": "B. L. Kashyap and Sons Limited",
    "ticker": "BLKASHYAP",
    "yf": "BLKASHYAP.NS"
  },
  {
    "name": "BLS International Services Limited",
    "ticker": "BLS",
    "yf": "BLS.NS"
  },
  {
    "name": "BLS E-Services Limited",
    "ticker": "BLSE",
    "yf": "BLSE.NS"
  },
  {
    "name": "Blue Dart Express Limited",
    "ticker": "BLUEDART",
    "yf": "BLUEDART.NS"
  },
  {
    "name": "Blue Jet Healthcare Limited",
    "ticker": "BLUEJET",
    "yf": "BLUEJET.NS"
  },
  {
    "name": "Blue Star Limited",
    "ticker": "BLUESTARCO",
    "yf": "BLUESTARCO.NS"
  },
  {
    "name": "BlueStone Jewellery and Lifestyle Limited",
    "ticker": "BLUESTONE",
    "yf": "BLUESTONE.NS"
  },
  {
    "name": "Bluspring Enterprises Limited",
    "ticker": "BLUSPRING",
    "yf": "BLUSPRING.NS"
  },
  {
    "name": "BMW Ventures Limited",
    "ticker": "BMWVENTLTD",
    "yf": "BMWVENTLTD.NS"
  },
  {
    "name": "BN Agrochem Limited",
    "ticker": "BNAGROCHEM",
    "yf": "BNAGROCHEM.NS"
  },
  {
    "name": "B & A Limited",
    "ticker": "BNALTD",
    "yf": "BNALTD.NS"
  },
  {
    "name": "Bodal Chemicals Limited",
    "ticker": "BODALCHEM",
    "yf": "BODALCHEM.NS"
  },
  {
    "name": "Bombay Dyeing & Mfg Company Limited",
    "ticker": "BOMDYEING",
    "yf": "BOMDYEING.NS"
  },
  {
    "name": "Bonlon Industries Limited",
    "ticker": "BONLON",
    "yf": "BONLON.NS"
  },
  {
    "name": "Borosil Limited",
    "ticker": "BOROLTD",
    "yf": "BOROLTD.NS"
  },
  {
    "name": "BOROSIL RENEWABLES LIMITED",
    "ticker": "BORORENEW",
    "yf": "BORORENEW.NS"
  },
  {
    "name": "Borosil Scientific Limited",
    "ticker": "BOROSCI",
    "yf": "BOROSCI.NS"
  },
  {
    "name": "BOSCH HOME COMFORT INDIA LIMITED",
    "ticker": "BOSCH-HCIL",
    "yf": "BOSCH-HCIL.NS"
  },
  {
    "name": "Bosch Limited",
    "ticker": "BOSCHLTD",
    "yf": "BOSCHLTD.NS"
  },
  {
    "name": "Bharat Petroleum Corporation Limited",
    "ticker": "BPCL",
    "yf": "BPCL.NS"
  },
  {
    "name": "BPL Limited",
    "ticker": "BPL",
    "yf": "BPL.NS"
  },
  {
    "name": "Brigade Enterprises Limited",
    "ticker": "BRIGADE",
    "yf": "BRIGADE.NS"
  },
  {
    "name": "Brigade Hotel Ventures Limited",
    "ticker": "BRIGHOTEL",
    "yf": "BRIGHOTEL.NS"
  },
  {
    "name": "Britannia Industries Limited",
    "ticker": "BRITANNIA",
    "yf": "BRITANNIA.NS"
  },
  {
    "name": "Bharat Road Network Limited",
    "ticker": "BRNL",
    "yf": "BRNL.NS"
  },
  {
    "name": "BSE Limited",
    "ticker": "BSE",
    "yf": "BSE.NS"
  },
  {
    "name": "Bombay Super Hybrid Seeds Limited",
    "ticker": "BSHSL",
    "yf": "BSHSL.NS"
  },
  {
    "name": "BSL Limited",
    "ticker": "BSL",
    "yf": "BSL.NS"
  },
  {
    "name": "BIRLASOFT LIMITED",
    "ticker": "BSOFT",
    "yf": "BSOFT.NS"
  },
  {
    "name": "Bodhi Tree Multimedia Limited",
    "ticker": "BTML",
    "yf": "BTML.NS"
  },
  {
    "name": "Bhilwara Technical Textiles Limited",
    "ticker": "BTTL",
    "yf": "BTTL.NS"
  },
  {
    "name": "Shankara Buildpro Limited",
    "ticker": "BUILDPRO",
    "yf": "BUILDPRO.NS"
  },
  {
    "name": "Butterfly Gandhimathi Appliances Limited",
    "ticker": "BUTTERFLY",
    "yf": "BUTTERFLY.NS"
  },
  {
    "name": "Barak Valley Cements Limited",
    "ticker": "BVCL",
    "yf": "BVCL.NS"
  },
  {
    "name": "California Software Company Limited",
    "ticker": "CALSOFT",
    "yf": "CALSOFT.NS"
  },
  {
    "name": "Camlin Fine Sciences Limited",
    "ticker": "CAMLINFINE",
    "yf": "CAMLINFINE.NS"
  },
  {
    "name": "Campus Activewear Limited",
    "ticker": "CAMPUS",
    "yf": "CAMPUS.NS"
  },
  {
    "name": "Computer Age Management Services Limited",
    "ticker": "CAMS",
    "yf": "CAMS.NS"
  },
  {
    "name": "Canara Bank",
    "ticker": "CANBK",
    "yf": "CANBK.NS"
  },
  {
    "name": "Can Fin Homes Limited",
    "ticker": "CANFINHOME",
    "yf": "CANFINHOME.NS"
  },
  {
    "name": "Canara HSBC Life Insurance Company Limited",
    "ticker": "CANHLIFE",
    "yf": "CANHLIFE.NS"
  },
  {
    "name": "Cantabil Retail India Limited",
    "ticker": "CANTABIL",
    "yf": "CANTABIL.NS"
  },
  {
    "name": "Capacit'e Infraprojects Limited",
    "ticker": "CAPACITE",
    "yf": "CAPACITE.NS"
  },
  {
    "name": "Capillary Technologies India Limited",
    "ticker": "CAPILLARY",
    "yf": "CAPILLARY.NS"
  },
  {
    "name": "Capital Small Finance Bank Limited",
    "ticker": "CAPITALSFB",
    "yf": "CAPITALSFB.NS"
  },
  {
    "name": "Caplin Point Laboratories Limited",
    "ticker": "CAPLIPOINT",
    "yf": "CAPLIPOINT.NS"
  },
  {
    "name": "Carborundum Universal Limited",
    "ticker": "CARBORUNIV",
    "yf": "CARBORUNIV.NS"
  },
  {
    "name": "CARE Ratings Limited",
    "ticker": "CARERATING",
    "yf": "CARERATING.NS"
  },
  {
    "name": "Carraro India Limited",
    "ticker": "CARRARO",
    "yf": "CARRARO.NS"
  },
  {
    "name": "Cartrade Tech Limited",
    "ticker": "CARTRADE",
    "yf": "CARTRADE.NS"
  },
  {
    "name": "CARYSIL LIMITED",
    "ticker": "CARYSIL",
    "yf": "CARYSIL.NS"
  },
  {
    "name": "Castrol India Limited",
    "ticker": "CASTROLIND",
    "yf": "CASTROLIND.NS"
  },
  {
    "name": "AvenuesAI Limited",
    "ticker": "CCAVENUE",
    "yf": "CCAVENUE.NS"
  },
  {
    "name": "Consolidated Construction Consortium Limited",
    "ticker": "CCCL",
    "yf": "CCCL.NS"
  },
  {
    "name": "Country Club Hospitality & Holidays Limited",
    "ticker": "CCHHL",
    "yf": "CCHHL.NS"
  },
  {
    "name": "CCL Products (India) Limited",
    "ticker": "CCL",
    "yf": "CCL.NS"
  },
  {
    "name": "Central Depository Services (India) Limited",
    "ticker": "CDSL",
    "yf": "CDSL.NS"
  },
  {
    "name": "CEAT Limited",
    "ticker": "CEATLTD",
    "yf": "CEATLTD.NS"
  },
  {
    "name": "Ceigall India Limited",
    "ticker": "CEIGALL",
    "yf": "CEIGALL.NS"
  },
  {
    "name": "Ceinsys Tech Limited",
    "ticker": "CEINSYS",
    "yf": "CEINSYS.NS"
  },
  {
    "name": "Celebrity Fashions Limited",
    "ticker": "CELEBRITY",
    "yf": "CELEBRITY.NS"
  },
  {
    "name": "Cello World Limited",
    "ticker": "CELLO",
    "yf": "CELLO.NS"
  },
  {
    "name": "Cemindia Projects Limited",
    "ticker": "CEMPRO",
    "yf": "CEMPRO.NS"
  },
  {
    "name": "Century Enka Limited",
    "ticker": "CENTENKA",
    "yf": "CENTENKA.NS"
  },
  {
    "name": "Century Extrusions Limited",
    "ticker": "CENTEXT",
    "yf": "CENTEXT.NS"
  },
  {
    "name": "Central Bank of India",
    "ticker": "CENTRALBK",
    "yf": "CENTRALBK.NS"
  },
  {
    "name": "Centrum Capital Limited",
    "ticker": "CENTRUM",
    "yf": "CENTRUM.NS"
  },
  {
    "name": "Centum Electronics Limited",
    "ticker": "CENTUM",
    "yf": "CENTUM.NS"
  },
  {
    "name": "Century Plyboards (India) Limited",
    "ticker": "CENTURYPLY",
    "yf": "CENTURYPLY.NS"
  },
  {
    "name": "Cera Sanitaryware Limited",
    "ticker": "CERA",
    "yf": "CERA.NS"
  },
  {
    "name": "CESC Limited",
    "ticker": "CESC",
    "yf": "CESC.NS"
  },
  {
    "name": "Concord Enviro Systems Limited",
    "ticker": "CEWATER",
    "yf": "CEWATER.NS"
  },
  {
    "name": "Capri Global Capital Limited",
    "ticker": "CGCL",
    "yf": "CGCL.NS"
  },
  {
    "name": "CG Power and Industrial Solutions Limited",
    "ticker": "CGPOWER",
    "yf": "CGPOWER.NS"
  },
  {
    "name": "Chalet Hotels Limited",
    "ticker": "CHALET",
    "yf": "CHALET.NS"
  },
  {
    "name": "Chambal Fertilizers & Chemicals Limited",
    "ticker": "CHAMBLFERT",
    "yf": "CHAMBLFERT.NS"
  },
  {
    "name": "Chembond Material Technologies Limited",
    "ticker": "CHEMBOND",
    "yf": "CHEMBOND.NS"
  },
  {
    "name": "Chembond Chemicals Limited",
    "ticker": "CHEMBONDCH",
    "yf": "CHEMBONDCH.NS"
  },
  {
    "name": "Chemcon Speciality Chemicals Limited",
    "ticker": "CHEMCON",
    "yf": "CHEMCON.NS"
  },
  {
    "name": "Chemfab Alkalis Limited",
    "ticker": "CHEMFAB",
    "yf": "CHEMFAB.NS"
  },
  {
    "name": "Chemplast Sanmar Limited",
    "ticker": "CHEMPLASTS",
    "yf": "CHEMPLASTS.NS"
  },
  {
    "name": "Chennai Petroleum Corporation Limited",
    "ticker": "CHENNPETRO",
    "yf": "CHENNPETRO.NS"
  },
  {
    "name": "Cheviot Company Limited",
    "ticker": "CHEVIOT",
    "yf": "CHEVIOT.NS"
  },
  {
    "name": "Choice International Limited",
    "ticker": "CHOICEIN",
    "yf": "CHOICEIN.NS"
  },
  {
    "name": "Cholamandalam Investment and Finance Company Limited",
    "ticker": "CHOLAFIN",
    "yf": "CHOLAFIN.NS"
  },
  {
    "name": "Cholamandalam Financial Holdings Limited",
    "ticker": "CHOLAHLDNG",
    "yf": "CHOLAHLDNG.NS"
  },
  {
    "name": "CIE Automotive India Limited",
    "ticker": "CIEINDIA",
    "yf": "CIEINDIA.NS"
  },
  {
    "name": "Capital India Finance Limited",
    "ticker": "CIFL",
    "yf": "CIFL.NS"
  },
  {
    "name": "Cigniti Technologies Limited",
    "ticker": "CIGNITITEC",
    "yf": "CIGNITITEC.NS"
  },
  {
    "name": "Cineline India Limited",
    "ticker": "CINELINE",
    "yf": "CINELINE.NS"
  },
  {
    "name": "Cinevista Limited",
    "ticker": "CINEVISTA",
    "yf": "CINEVISTA.NS"
  },
  {
    "name": "Cipla Limited",
    "ticker": "CIPLA",
    "yf": "CIPLA.NS"
  },
  {
    "name": "Clean Science and Technology Limited",
    "ticker": "CLEAN",
    "yf": "CLEAN.NS"
  },
  {
    "name": "Clean Max Enviro Energy Solutions Limited",
    "ticker": "CLEANMAX",
    "yf": "CLEANMAX.NS"
  },
  {
    "name": "Chaman Lal Setia Exports Limited",
    "ticker": "CLSEL",
    "yf": "CLSEL.NS"
  },
  {
    "name": "Central Mine Planning & Design Institute Limited",
    "ticker": "CMPDI",
    "yf": "CMPDI.NS"
  },
  {
    "name": "CMS Info Systems Limited",
    "ticker": "CMSINFO",
    "yf": "CMSINFO.NS"
  },
  {
    "name": "Creative Newtech Limited",
    "ticker": "CNL",
    "yf": "CNL.NS"
  },
  {
    "name": "Coal India Limited",
    "ticker": "COALINDIA",
    "yf": "COALINDIA.NS"
  },
  {
    "name": "Coastal Corporation Limited",
    "ticker": "COASTCORP",
    "yf": "COASTCORP.NS"
  },
  {
    "name": "Cochin Shipyard Limited",
    "ticker": "COCHINSHIP",
    "yf": "COCHINSHIP.NS"
  },
  {
    "name": "John Cockerill India Limited",
    "ticker": "COCKERILL",
    "yf": "COCKERILL.NS"
  },
  {
    "name": "Coffee Day Enterprises Limited",
    "ticker": "COFFEEDAY",
    "yf": "COFFEEDAY.NS"
  },
  {
    "name": "Coforge Limited",
    "ticker": "COFORGE",
    "yf": "COFORGE.NS"
  },
  {
    "name": "Cohance Lifesciences Limited",
    "ticker": "COHANCE",
    "yf": "COHANCE.NS"
  },
  {
    "name": "Colgate Palmolive (India) Limited",
    "ticker": "COLPAL",
    "yf": "COLPAL.NS"
  },
  {
    "name": "Comfort Intech Limited",
    "ticker": "COMFINTE",
    "yf": "COMFINTE.NS"
  },
  {
    "name": "Compucom Software Limited",
    "ticker": "COMPUSOFT",
    "yf": "COMPUSOFT.NS"
  },
  {
    "name": "Commercial Syn Bags Limited",
    "ticker": "COMSYN",
    "yf": "COMSYN.NS"
  },
  {
    "name": "Container Corporation of India Limited",
    "ticker": "CONCOR",
    "yf": "CONCOR.NS"
  },
  {
    "name": "Concord Biotech Limited",
    "ticker": "CONCORDBIO",
    "yf": "CONCORDBIO.NS"
  },
  {
    "name": "Confidence Petroleum India Limited",
    "ticker": "CONFIPET",
    "yf": "CONFIPET.NS"
  },
  {
    "name": "Control Print Limited",
    "ticker": "CONTROLPR",
    "yf": "CONTROLPR.NS"
  },
  {
    "name": "Coral India Finance & Housing Limited",
    "ticker": "CORALFINAC",
    "yf": "CORALFINAC.NS"
  },
  {
    "name": "Cords Cable Industries Limited",
    "ticker": "CORDSCABLE",
    "yf": "CORDSCABLE.NS"
  },
  {
    "name": "Coromandel International Limited",
    "ticker": "COROMANDEL",
    "yf": "COROMANDEL.NS"
  },
  {
    "name": "CORONA Remedies Limited",
    "ticker": "CORONA",
    "yf": "CORONA.NS"
  },
  {
    "name": "COSMO FIRST LIMITED",
    "ticker": "COSMOFIRST",
    "yf": "COSMOFIRST.NS"
  },
  {
    "name": "Country Condo's Limited",
    "ticker": "COUNCODOS",
    "yf": "COUNCODOS.NS"
  },
  {
    "name": "CP Capital Limited",
    "ticker": "CPCAP",
    "yf": "CPCAP.NS"
  },
  {
    "name": "Career Point Edutech Limited",
    "ticker": "CPEDU",
    "yf": "CPEDU.NS"
  },
  {
    "name": "Aditya Infotech Limited",
    "ticker": "CPPLUS",
    "yf": "CPPLUS.NS"
  },
  {
    "name": "Craftsman Automation Limited",
    "ticker": "CRAFTSMAN",
    "yf": "CRAFTSMAN.NS"
  },
  {
    "name": "Canara Robeco Asset Management Company Limited",
    "ticker": "CRAMC",
    "yf": "CRAMC.NS"
  },
  {
    "name": "Creative Eye Limited",
    "ticker": "CREATIVEYE",
    "yf": "CREATIVEYE.NS"
  },
  {
    "name": "CREDITACCESS GRAMEEN LIMITED",
    "ticker": "CREDITACC",
    "yf": "CREDITACC.NS"
  },
  {
    "name": "Crest Ventures Limited",
    "ticker": "CREST",
    "yf": "CREST.NS"
  },
  {
    "name": "CRISIL Limited",
    "ticker": "CRISIL",
    "yf": "CRISIL.NS"
  },
  {
    "name": "Crizac Limited",
    "ticker": "CRIZAC",
    "yf": "CRIZAC.NS"
  },
  {
    "name": "Crompton Greaves Consumer Electricals Limited",
    "ticker": "CROMPTON",
    "yf": "CROMPTON.NS"
  },
  {
    "name": "Crown Lifters Limited",
    "ticker": "CROWN",
    "yf": "CROWN.NS"
  },
  {
    "name": "CSB Bank Limited",
    "ticker": "CSBBANK",
    "yf": "CSBBANK.NS"
  },
  {
    "name": "CSL Finance Limited",
    "ticker": "CSLFINANCE",
    "yf": "CSLFINANCE.NS"
  },
  {
    "name": "City Union Bank Limited",
    "ticker": "CUB",
    "yf": "CUB.NS"
  },
  {
    "name": "Cubex Tubings Limited",
    "ticker": "CUBEXTUB",
    "yf": "CUBEXTUB.NS"
  },
  {
    "name": "Cummins India Limited",
    "ticker": "CUMMINSIND",
    "yf": "CUMMINSIND.NS"
  },
  {
    "name": "Cupid Limited",
    "ticker": "CUPID",
    "yf": "CUPID.NS"
  },
  {
    "name": "Cyber Media (India) Limited",
    "ticker": "CYBERMEDIA",
    "yf": "CYBERMEDIA.NS"
  },
  {
    "name": "Cybertech Systems And Software Limited",
    "ticker": "CYBERTECH",
    "yf": "CYBERTECH.NS"
  },
  {
    "name": "Cyient Limited",
    "ticker": "CYIENT",
    "yf": "CYIENT.NS"
  },
  {
    "name": "Cyient DLM Limited",
    "ticker": "CYIENTDLM",
    "yf": "CYIENTDLM.NS"
  },
  {
    "name": "Dabur India Limited",
    "ticker": "DABUR",
    "yf": "DABUR.NS"
  },
  {
    "name": "Dai-Ichi Karkaria Limited",
    "ticker": "DAICHI",
    "yf": "DAICHI.NS"
  },
  {
    "name": "Dalmia Bharat Limited",
    "ticker": "DALBHARAT",
    "yf": "DALBHARAT.NS"
  },
  {
    "name": "Dalmia Bharat Sugar and Industries Limited",
    "ticker": "DALMIASUG",
    "yf": "DALMIASUG.NS"
  },
  {
    "name": "Dam Capital Advisors Limited",
    "ticker": "DAMCAPITAL",
    "yf": "DAMCAPITAL.NS"
  },
  {
    "name": "Damodar Industries Limited",
    "ticker": "DAMODARIND",
    "yf": "DAMODARIND.NS"
  },
  {
    "name": "Dangee Dums Limited",
    "ticker": "DANGEE",
    "yf": "DANGEE.NS"
  },
  {
    "name": "Datamatics Global Services Limited",
    "ticker": "DATAMATICS",
    "yf": "DATAMATICS.NS"
  },
  {
    "name": "Data Patterns (India) Limited",
    "ticker": "DATAPATTNS",
    "yf": "DATAPATTNS.NS"
  },
  {
    "name": "Davangere Sugar Company Limited",
    "ticker": "DAVANGERE",
    "yf": "DAVANGERE.NS"
  },
  {
    "name": "D.B.Corp Limited",
    "ticker": "DBCORP",
    "yf": "DBCORP.NS"
  },
  {
    "name": "Deepak Builders & Engineers India Limited",
    "ticker": "DBEIL",
    "yf": "DBEIL.NS"
  },
  {
    "name": "Dilip Buildcon Limited",
    "ticker": "DBL",
    "yf": "DBL.NS"
  },
  {
    "name": "Valor Estate Limited",
    "ticker": "DBREALTY",
    "yf": "DBREALTY.NS"
  },
  {
    "name": "DB (International) Stock Brokers Limited",
    "ticker": "DBSTOCKBRO",
    "yf": "DBSTOCKBRO.NS"
  },
  {
    "name": "Dishman Carbogen Amcis Limited",
    "ticker": "DCAL",
    "yf": "DCAL.NS"
  },
  {
    "name": "DCB Bank Limited",
    "ticker": "DCBBANK",
    "yf": "DCBBANK.NS"
  },
  {
    "name": "DCM  Limited",
    "ticker": "DCM",
    "yf": "DCM.NS"
  },
  {
    "name": "DCM Nouvelle Limited",
    "ticker": "DCMNVL",
    "yf": "DCMNVL.NS"
  },
  {
    "name": "DCM Shriram Limited",
    "ticker": "DCMSHRIRAM",
    "yf": "DCMSHRIRAM.NS"
  },
  {
    "name": "DCM Shriram Industries Limited",
    "ticker": "DCMSRIND",
    "yf": "DCMSRIND.NS"
  },
  {
    "name": "DCW Limited",
    "ticker": "DCW",
    "yf": "DCW.NS"
  },
  {
    "name": "DCX Systems Limited",
    "ticker": "DCXINDIA",
    "yf": "DCXINDIA.NS"
  },
  {
    "name": "Ddev Plastiks Industries Limited",
    "ticker": "DDEVPLSTIK",
    "yf": "DDEVPLSTIK.NS"
  },
  {
    "name": "Deccan Cements Limited",
    "ticker": "DECCANCE",
    "yf": "DECCANCE.NS"
  },
  {
    "name": "Deccan Gold Mines Limited",
    "ticker": "DECNGOLD",
    "yf": "DECNGOLD.NS"
  },
  {
    "name": "DEE Development Engineers Limited",
    "ticker": "DEEDEV",
    "yf": "DEEDEV.NS"
  },
  {
    "name": "Deepak Fertilizers and Petrochemicals Corporation Limited",
    "ticker": "DEEPAKFERT",
    "yf": "DEEPAKFERT.NS"
  },
  {
    "name": "Deepak Nitrite Limited",
    "ticker": "DEEPAKNTR",
    "yf": "DEEPAKNTR.NS"
  },
  {
    "name": "Deep Industries Limited",
    "ticker": "DEEPINDS",
    "yf": "DEEPINDS.NS"
  },
  {
    "name": "Delhivery Limited",
    "ticker": "DELHIVERY",
    "yf": "DELHIVERY.NS"
  },
  {
    "name": "DELPHI WORLD MONEY LIMITED",
    "ticker": "DELPHIFX",
    "yf": "DELPHIFX.NS"
  },
  {
    "name": "Delta Corp Limited",
    "ticker": "DELTACORP",
    "yf": "DELTACORP.NS"
  },
  {
    "name": "Delta Manufacturing Limited",
    "ticker": "DELTAMAGNT",
    "yf": "DELTAMAGNT.NS"
  },
  {
    "name": "Den Networks Limited",
    "ticker": "DEN",
    "yf": "DEN.NS"
  },
  {
    "name": "De Nora India Limited",
    "ticker": "DENORA",
    "yf": "DENORA.NS"
  },
  {
    "name": "Denta Water and Infra Solutions Limited",
    "ticker": "DENTA",
    "yf": "DENTA.NS"
  },
  {
    "name": "Dev Information Technology Limited",
    "ticker": "DEVIT",
    "yf": "DEVIT.NS"
  },
  {
    "name": "Dev Accelerator Limited",
    "ticker": "DEVX",
    "yf": "DEVX.NS"
  },
  {
    "name": "Devyani International Limited",
    "ticker": "DEVYANI",
    "yf": "DEVYANI.NS"
  },
  {
    "name": "Digicontent Limited",
    "ticker": "DGCONTENT",
    "yf": "DGCONTENT.NS"
  },
  {
    "name": "Dhampur Sugar Mills Limited",
    "ticker": "DHAMPURSUG",
    "yf": "DHAMPURSUG.NS"
  },
  {
    "name": "Dhanlaxmi Bank Limited",
    "ticker": "DHANBANK",
    "yf": "DHANBANK.NS"
  },
  {
    "name": "Dhanuka Agritech Limited",
    "ticker": "DHANUKA",
    "yf": "DHANUKA.NS"
  },
  {
    "name": "Dharmaj Crop Guard Limited",
    "ticker": "DHARMAJ",
    "yf": "DHARMAJ.NS"
  },
  {
    "name": "Dhruv Consultancy Services Limited",
    "ticker": "DHRUV",
    "yf": "DHRUV.NS"
  },
  {
    "name": "Dhunseri Investments Limited",
    "ticker": "DHUNINV",
    "yf": "DHUNINV.NS"
  },
  {
    "name": "Diamond Power Infrastructure Limited",
    "ticker": "DIACABS",
    "yf": "DIACABS.NS"
  },
  {
    "name": "Diamines & Chemicals Limited",
    "ticker": "DIAMINESQ",
    "yf": "DIAMINESQ.NS"
  },
  {
    "name": "Prataap Snacks Limited",
    "ticker": "DIAMONDYD",
    "yf": "DIAMONDYD.NS"
  },
  {
    "name": "DIC India Limited",
    "ticker": "DICIND",
    "yf": "DICIND.NS"
  },
  {
    "name": "Diffusion Engineers Limited",
    "ticker": "DIFFNKG",
    "yf": "DIFFNKG.NS"
  },
  {
    "name": "Digidrive Distributors Limited",
    "ticker": "DIGIDRIVE",
    "yf": "DIGIDRIVE.NS"
  },
  {
    "name": "Digitide Solutions Limited",
    "ticker": "DIGITIDE",
    "yf": "DIGITIDE.NS"
  },
  {
    "name": "Digjam Limited",
    "ticker": "DIGJAMLMTD",
    "yf": "DIGJAMLMTD.NS"
  },
  {
    "name": "Disa India Limited",
    "ticker": "DISAQ",
    "yf": "DISAQ.NS"
  },
  {
    "name": "Divgi Torqtransfer Systems Limited",
    "ticker": "DIVGIITTS",
    "yf": "DIVGIITTS.NS"
  },
  {
    "name": "Divi's Laboratories Limited",
    "ticker": "DIVISLAB",
    "yf": "DIVISLAB.NS"
  },
  {
    "name": "Dixon Technologies (India) Limited",
    "ticker": "DIXON",
    "yf": "DIXON.NS"
  },
  {
    "name": "DLF Limited",
    "ticker": "DLF",
    "yf": "DLF.NS"
  },
  {
    "name": "D-Link (India) Limited",
    "ticker": "DLINKINDIA",
    "yf": "DLINKINDIA.NS"
  },
  {
    "name": "Avenue Supermarts Limited",
    "ticker": "DMART",
    "yf": "DMART.NS"
  },
  {
    "name": "DMCC SPECIALITY CHEMICALS LIMITED",
    "ticker": "DMCC",
    "yf": "DMCC.NS"
  },
  {
    "name": "Diligent Media Corporation Limited",
    "ticker": "DNAMEDIA",
    "yf": "DNAMEDIA.NS"
  },
  {
    "name": "Dodla Dairy Limited",
    "ticker": "DODLA",
    "yf": "DODLA.NS"
  },
  {
    "name": "Dolat Algotech Limited",
    "ticker": "DOLATALGO",
    "yf": "DOLATALGO.NS"
  },
  {
    "name": "Dollar Industries Limited",
    "ticker": "DOLLAR",
    "yf": "DOLLAR.NS"
  },
  {
    "name": "Dolphin Offshore Enterprises (India) Limited",
    "ticker": "DOLPHIN",
    "yf": "DOLPHIN.NS"
  },
  {
    "name": "DOMS Industries Limited",
    "ticker": "DOMS",
    "yf": "DOMS.NS"
  },
  {
    "name": "Donear Industries Limited",
    "ticker": "DONEAR",
    "yf": "DONEAR.NS"
  },
  {
    "name": "D. P. Abhushan Limited",
    "ticker": "DPABHUSHAN",
    "yf": "DPABHUSHAN.NS"
  },
  {
    "name": "DPSC Limited",
    "ticker": "DPSCLTD",
    "yf": "DPSCLTD.NS"
  },
  {
    "name": "D P Wires Limited",
    "ticker": "DPWIRES",
    "yf": "DPWIRES.NS"
  },
  {
    "name": "Dr Agarwals Eye Hospital Limited",
    "ticker": "DRAGARWQ",
    "yf": "DRAGARWQ.NS"
  },
  {
    "name": "DRC Systems India Limited",
    "ticker": "DRCSYSTEMS",
    "yf": "DRCSYSTEMS.NS"
  },
  {
    "name": "Dreamfolks Services Limited",
    "ticker": "DREAMFOLKS",
    "yf": "DREAMFOLKS.NS"
  },
  {
    "name": "Dredging Corporation of India Limited",
    "ticker": "DREDGECORP",
    "yf": "DREDGECORP.NS"
  },
  {
    "name": "Dr. Reddy's Laboratories Limited",
    "ticker": "DRREDDY",
    "yf": "DRREDDY.NS"
  },
  {
    "name": "DCM Shriram Fine Chemicals Limited",
    "ticker": "DSFCL",
    "yf": "DSFCL.NS"
  },
  {
    "name": "Dynacons Systems & Solutions Limited",
    "ticker": "DSSL",
    "yf": "DSSL.NS"
  },
  {
    "name": "Dhunseri Tea & Industries Limited",
    "ticker": "DTIL",
    "yf": "DTIL.NS"
  },
  {
    "name": "Dhunseri Ventures Limited",
    "ticker": "DVL",
    "yf": "DVL.NS"
  },
  {
    "name": "Dwarikesh Sugar Industries Limited",
    "ticker": "DWARKESH",
    "yf": "DWARKESH.NS"
  },
  {
    "name": "Dynamic Cables Limited",
    "ticker": "DYCL",
    "yf": "DYCL.NS"
  },
  {
    "name": "Dynamatic Technologies Limited",
    "ticker": "DYNAMATECH",
    "yf": "DYNAMATECH.NS"
  },
  {
    "name": "Dynemic Products Limited",
    "ticker": "DYNPRO",
    "yf": "DYNPRO.NS"
  },
  {
    "name": "Easy Trip Planners Limited",
    "ticker": "EASEMYTRIP",
    "yf": "EASEMYTRIP.NS"
  },
  {
    "name": "GNG Electronics Limited",
    "ticker": "EBGNG",
    "yf": "EBGNG.NS"
  },
  {
    "name": "eClerx Services Limited",
    "ticker": "ECLERX",
    "yf": "ECLERX.NS"
  },
  {
    "name": "Ecos (India) Mobility & Hospitality Limited",
    "ticker": "ECOSMOBLTY",
    "yf": "ECOSMOBLTY.NS"
  },
  {
    "name": "Edelweiss Financial Services Limited",
    "ticker": "EDELWEISS",
    "yf": "EDELWEISS.NS"
  },
  {
    "name": "EFC (I) Limited",
    "ticker": "EFCIL",
    "yf": "EFCIL.NS"
  },
  {
    "name": "Eicher Motors Limited",
    "ticker": "EICHERMOT",
    "yf": "EICHERMOT.NS"
  },
  {
    "name": "EID Parry India Limited",
    "ticker": "EIDPARRY",
    "yf": "EIDPARRY.NS"
  },
  {
    "name": "Enviro Infra Engineers Limited",
    "ticker": "EIEL",
    "yf": "EIEL.NS"
  },
  {
    "name": "Euro India Fresh Foods Limited",
    "ticker": "EIFFL",
    "yf": "EIFFL.NS"
  },
  {
    "name": "EIH Associated Hotels Limited",
    "ticker": "EIHAHOTELS",
    "yf": "EIHAHOTELS.NS"
  },
  {
    "name": "EIH Limited",
    "ticker": "EIHOTEL",
    "yf": "EIHOTEL.NS"
  },
  {
    "name": "Eimco Elecon (India) Limited",
    "ticker": "EIMCOELECO",
    "yf": "EIMCOELECO.NS"
  },
  {
    "name": "Everest Kanto Cylinder Limited",
    "ticker": "EKC",
    "yf": "EKC.NS"
  },
  {
    "name": "Elantas Beck India Limited",
    "ticker": "ELANTAS",
    "yf": "ELANTAS.NS"
  },
  {
    "name": "EL CID Investments Limited",
    "ticker": "ELCIDIN",
    "yf": "ELCIDIN.NS"
  },
  {
    "name": "Eldeco Housing And Industries Limited",
    "ticker": "ELDEHSG",
    "yf": "ELDEHSG.NS"
  },
  {
    "name": "Elecon Engineering Company Limited",
    "ticker": "ELECON",
    "yf": "ELECON.NS"
  },
  {
    "name": "Electrosteel Castings Limited",
    "ticker": "ELECTCAST",
    "yf": "ELECTCAST.NS"
  },
  {
    "name": "Electrotherm (India) Limited",
    "ticker": "ELECTHERM",
    "yf": "ELECTHERM.NS"
  },
  {
    "name": "Elgi Equipments Limited",
    "ticker": "ELGIEQUIP",
    "yf": "ELGIEQUIP.NS"
  },
  {
    "name": "Elgi Rubber Company Limited",
    "ticker": "ELGIRUBCO",
    "yf": "ELGIRUBCO.NS"
  },
  {
    "name": "Elin Electronics Limited",
    "ticker": "ELIN",
    "yf": "ELIN.NS"
  },
  {
    "name": "Elitecon International Limited",
    "ticker": "ELITECON",
    "yf": "ELITECON.NS"
  },
  {
    "name": "Ellenbarrie Industrial Gases Limited",
    "ticker": "ELLEN",
    "yf": "ELLEN.NS"
  },
  {
    "name": "Elpro International Limited",
    "ticker": "ELPROINTL",
    "yf": "ELPROINTL.NS"
  },
  {
    "name": "Emami Limited",
    "ticker": "EMAMILTD",
    "yf": "EMAMILTD.NS"
  },
  {
    "name": "Emami Paper Mills Limited",
    "ticker": "EMAMIPAP",
    "yf": "EMAMIPAP.NS"
  },
  {
    "name": "Emcure Pharmaceuticals Limited",
    "ticker": "EMCURE",
    "yf": "EMCURE.NS"
  },
  {
    "name": "Electronics Mart India Limited",
    "ticker": "EMIL",
    "yf": "EMIL.NS"
  },
  {
    "name": "Emkay Global Financial Services Limited",
    "ticker": "EMKAY",
    "yf": "EMKAY.NS"
  },
  {
    "name": "Emmbi Industries Limited",
    "ticker": "EMMBI",
    "yf": "EMMBI.NS"
  },
  {
    "name": "Emmvee Photovoltaic Power Limited",
    "ticker": "EMMVEE",
    "yf": "EMMVEE.NS"
  },
  {
    "name": "EMS Limited",
    "ticker": "EMSLIMITED",
    "yf": "EMSLIMITED.NS"
  },
  {
    "name": "eMudhra Limited",
    "ticker": "EMUDHRA",
    "yf": "EMUDHRA.NS"
  },
  {
    "name": "Endurance Technologies Limited",
    "ticker": "ENDURANCE",
    "yf": "ENDURANCE.NS"
  },
  {
    "name": "Energy Development Company Limited",
    "ticker": "ENERGYDEV",
    "yf": "ENERGYDEV.NS"
  },
  {
    "name": "Engineers India Limited",
    "ticker": "ENGINERSIN",
    "yf": "ENGINERSIN.NS"
  },
  {
    "name": "Entertainment Network (India) Limited",
    "ticker": "ENIL",
    "yf": "ENIL.NS"
  },
  {
    "name": "Siemens Energy India Limited",
    "ticker": "ENRIN",
    "yf": "ENRIN.NS"
  },
  {
    "name": "Entero Healthcare Solutions Limited",
    "ticker": "ENTERO",
    "yf": "ENTERO.NS"
  },
  {
    "name": "EPACK Durable Limited",
    "ticker": "EPACK",
    "yf": "EPACK.NS"
  },
  {
    "name": "EPack Prefab Technologies Limited",
    "ticker": "EPACKPEB",
    "yf": "EPACKPEB.NS"
  },
  {
    "name": "Epigral Limited",
    "ticker": "EPIGRAL",
    "yf": "EPIGRAL.NS"
  },
  {
    "name": "EPL Limited",
    "ticker": "EPL",
    "yf": "EPL.NS"
  },
  {
    "name": "Equitas Small Finance Bank Limited",
    "ticker": "EQUITASBNK",
    "yf": "EQUITASBNK.NS"
  },
  {
    "name": "Eris Lifesciences Limited",
    "ticker": "ERIS",
    "yf": "ERIS.NS"
  },
  {
    "name": "Esab India Limited",
    "ticker": "ESABINDIA",
    "yf": "ESABINDIA.NS"
  },
  {
    "name": "ESAF Small Finance Bank Limited",
    "ticker": "ESAFSFB",
    "yf": "ESAFSFB.NS"
  },
  {
    "name": "Escorts Kubota Limited",
    "ticker": "ESCORTS",
    "yf": "ESCORTS.NS"
  },
  {
    "name": "Essar Shipping Limited",
    "ticker": "ESSARSHPNG",
    "yf": "ESSARSHPNG.NS"
  },
  {
    "name": "Integra Essentia Limited",
    "ticker": "ESSENTIA",
    "yf": "ESSENTIA.NS"
  },
  {
    "name": "Ester Industries Limited",
    "ticker": "ESTER",
    "yf": "ESTER.NS"
  },
  {
    "name": "ETERNAL LIMITED",
    "ticker": "ETERNAL",
    "yf": "ETERNAL.NS"
  },
  {
    "name": "Ethos Limited",
    "ticker": "ETHOSLTD",
    "yf": "ETHOSLTD.NS"
  },
  {
    "name": "Eureka Forbes Limited",
    "ticker": "EUREKAFORB",
    "yf": "EUREKAFORB.NS"
  },
  {
    "name": "Euro Panel Products Limited",
    "ticker": "EUROBOND",
    "yf": "EUROBOND.NS"
  },
  {
    "name": "Euro Pratik Sales Limited",
    "ticker": "EUROPRATIK",
    "yf": "EUROPRATIK.NS"
  },
  {
    "name": "Eurotex Industries and Exports Limited",
    "ticker": "EUROTEXIND",
    "yf": "EUROTEXIND.NS"
  },
  {
    "name": "Eveready Industries India Limited",
    "ticker": "EVEREADY",
    "yf": "EVEREADY.NS"
  },
  {
    "name": "Everest Industries Limited",
    "ticker": "EVERESTIND",
    "yf": "EVERESTIND.NS"
  },
  {
    "name": "Excel Industries Limited",
    "ticker": "EXCELINDUS",
    "yf": "EXCELINDUS.NS"
  },
  {
    "name": "Excelsoft Technologies Limited",
    "ticker": "EXCELSOFT",
    "yf": "EXCELSOFT.NS"
  },
  {
    "name": "Exicom Tele-Systems Limited",
    "ticker": "EXICOM",
    "yf": "EXICOM.NS"
  },
  {
    "name": "Exide Industries Limited",
    "ticker": "EXIDEIND",
    "yf": "EXIDEIND.NS"
  },
  {
    "name": "Expleo Solutions Limited",
    "ticker": "EXPLEOSOL",
    "yf": "EXPLEOSOL.NS"
  },
  {
    "name": "Exxaro Tiles Limited",
    "ticker": "EXXARO",
    "yf": "EXXARO.NS"
  },
  {
    "name": "Fabtech Technologies Limited",
    "ticker": "FABTECH",
    "yf": "FABTECH.NS"
  },
  {
    "name": "Fertilizers and Chemicals Travancore Limited",
    "ticker": "FACT",
    "yf": "FACT.NS"
  },
  {
    "name": "Fairchem Organics Limited",
    "ticker": "FAIRCHEMOR",
    "yf": "FAIRCHEMOR.NS"
  },
  {
    "name": "Fineotex Chemical Limited",
    "ticker": "FCL",
    "yf": "FCL.NS"
  },
  {
    "name": "FDC Limited",
    "ticker": "FDC",
    "yf": "FDC.NS"
  },
  {
    "name": "Fedders Holding Limited",
    "ticker": "FEDDERSHOL",
    "yf": "FEDDERSHOL.NS"
  },
  {
    "name": "The Federal Bank  Limited",
    "ticker": "FEDERALBNK",
    "yf": "FEDERALBNK.NS"
  },
  {
    "name": "Fedbank Financial Services Limited",
    "ticker": "FEDFINA",
    "yf": "FEDFINA.NS"
  },
  {
    "name": "Fermenta Biotech Limited",
    "ticker": "FERMENTA",
    "yf": "FERMENTA.NS"
  },
  {
    "name": "Fiem Industries Limited",
    "ticker": "FIEMIND",
    "yf": "FIEMIND.NS"
  },
  {
    "name": "Filatex India Limited",
    "ticker": "FILATEX",
    "yf": "FILATEX.NS"
  },
  {
    "name": "Finolex Cables Limited",
    "ticker": "FINCABLES",
    "yf": "FINCABLES.NS"
  },
  {
    "name": "Fine Organic Industries Limited",
    "ticker": "FINEORG",
    "yf": "FINEORG.NS"
  },
  {
    "name": "Finkurve Financial Services Limited",
    "ticker": "FINKURVE",
    "yf": "FINKURVE.NS"
  },
  {
    "name": "Fino Payments Bank Limited",
    "ticker": "FINOPB",
    "yf": "FINOPB.NS"
  },
  {
    "name": "Finolex Industries Limited",
    "ticker": "FINPIPE",
    "yf": "FINPIPE.NS"
  },
  {
    "name": "Brainbees Solutions Limited",
    "ticker": "FIRSTCRY",
    "yf": "FIRSTCRY.NS"
  },
  {
    "name": "Fischer Medical Ventures Limited",
    "ticker": "FISCHER",
    "yf": "FISCHER.NS"
  },
  {
    "name": "Five-Star Business Finance Limited",
    "ticker": "FIVESTAR",
    "yf": "FIVESTAR.NS"
  },
  {
    "name": "Flair Writing Industries Limited",
    "ticker": "FLAIR",
    "yf": "FLAIR.NS"
  },
  {
    "name": "Flexituff Ventures International Limited",
    "ticker": "FLEXITUFF",
    "yf": "FLEXITUFF.NS"
  },
  {
    "name": "Gujarat Fluorochemicals Limited",
    "ticker": "FLUOROCHEM",
    "yf": "FLUOROCHEM.NS"
  },
  {
    "name": "Federal-Mogul Goetze (India) Limited.",
    "ticker": "FMGOETZE",
    "yf": "FMGOETZE.NS"
  },
  {
    "name": "Future Market Networks Limited",
    "ticker": "FMNL",
    "yf": "FMNL.NS"
  },
  {
    "name": "Focus Lighting and Fixtures Limited",
    "ticker": "FOCUS",
    "yf": "FOCUS.NS"
  },
  {
    "name": "Foods & Inns Limited",
    "ticker": "FOODSIN",
    "yf": "FOODSIN.NS"
  },
  {
    "name": "FORCE MOTORS LTD",
    "ticker": "FORCEMOT",
    "yf": "FORCEMOT.NS"
  },
  {
    "name": "Fortis Healthcare Limited",
    "ticker": "FORTIS",
    "yf": "FORTIS.NS"
  },
  {
    "name": "Foseco India Limited",
    "ticker": "FOSECOIND",
    "yf": "FOSECOIND.NS"
  },
  {
    "name": "Fractal Analytics Limited",
    "ticker": "FRACTAL",
    "yf": "FRACTAL.NS"
  },
  {
    "name": "Frontier Springs Limited",
    "ticker": "FRONTSP",
    "yf": "FRONTSP.NS"
  },
  {
    "name": "Firstsource Solutions Limited",
    "ticker": "FSL",
    "yf": "FSL.NS"
  },
  {
    "name": "Fusion Finance Limited",
    "ticker": "FUSION",
    "yf": "FUSION.NS"
  },
  {
    "name": "Gabriel India Limited",
    "ticker": "GABRIEL",
    "yf": "GABRIEL.NS"
  },
  {
    "name": "Gujarat Ambuja Exports Limited",
    "ticker": "GAEL",
    "yf": "GAEL.NS"
  },
  {
    "name": "GAIL (India) Limited",
    "ticker": "GAIL",
    "yf": "GAIL.NS"
  },
  {
    "name": "Gala Precision Engineering Limited",
    "ticker": "GALAPREC",
    "yf": "GALAPREC.NS"
  },
  {
    "name": "Galaxy Surfactants Limited",
    "ticker": "GALAXYSURF",
    "yf": "GALAXYSURF.NS"
  },
  {
    "name": "Gallantt Ispat Limited",
    "ticker": "GALLANTT",
    "yf": "GALLANTT.NS"
  },
  {
    "name": "Gandhar Oil Refinery (India) Limited",
    "ticker": "GANDHAR",
    "yf": "GANDHAR.NS"
  },
  {
    "name": "Gandhi Special Tubes Limited",
    "ticker": "GANDHITUBE",
    "yf": "GANDHITUBE.NS"
  },
  {
    "name": "Ganesha Ecosphere Limited",
    "ticker": "GANECOS",
    "yf": "GANECOS.NS"
  },
  {
    "name": "Ganesh Benzoplast Limited",
    "ticker": "GANESHBE",
    "yf": "GANESHBE.NS"
  },
  {
    "name": "Ganesh Consumer Products Limited",
    "ticker": "GANESHCP",
    "yf": "GANESHCP.NS"
  },
  {
    "name": "GANESH HOUSING LIMITED",
    "ticker": "GANESHHOU",
    "yf": "GANESHHOU.NS"
  },
  {
    "name": "Ganga Forging Limited",
    "ticker": "GANGAFORGE",
    "yf": "GANGAFORGE.NS"
  },
  {
    "name": "Ganges Securities Limited",
    "ticker": "GANGESSECU",
    "yf": "GANGESSECU.NS"
  },
  {
    "name": "Garware Technical Fibres Limited",
    "ticker": "GARFIBRES",
    "yf": "GARFIBRES.NS"
  },
  {
    "name": "Garuda Construction and Engineering Limited",
    "ticker": "GARUDA",
    "yf": "GARUDA.NS"
  },
  {
    "name": "GACM Technologies Limited",
    "ticker": "GATECH",
    "yf": "GATECH.NS"
  },
  {
    "name": "GACM Technologies Limited",
    "ticker": "GATECHDVR",
    "yf": "GATECHDVR.NS"
  },
  {
    "name": "Gateway Distriparks Limited",
    "ticker": "GATEWAY",
    "yf": "GATEWAY.NS"
  },
  {
    "name": "Gayatri Highways Limited",
    "ticker": "GAYAHWS",
    "yf": "GAYAHWS.NS"
  },
  {
    "name": "Gretex Corporate Services Limited",
    "ticker": "GCSL",
    "yf": "GCSL.NS"
  },
  {
    "name": "GeeCee Ventures Limited",
    "ticker": "GEECEE",
    "yf": "GEECEE.NS"
  },
  {
    "name": "Geekay Wires Limited",
    "ticker": "GEEKAYWIRE",
    "yf": "GEEKAYWIRE.NS"
  },
  {
    "name": "Generic Engineering Construction and Projects Limited",
    "ticker": "GENCON",
    "yf": "GENCON.NS"
  },
  {
    "name": "Genesys International Corporation Limited",
    "ticker": "GENESYS",
    "yf": "GENESYS.NS"
  },
  {
    "name": "Genus Paper & Boards Limited",
    "ticker": "GENUSPAPER",
    "yf": "GENUSPAPER.NS"
  },
  {
    "name": "Genus Power Infrastructures Limited",
    "ticker": "GENUSPOWER",
    "yf": "GENUSPOWER.NS"
  },
  {
    "name": "Geojit Financial Services Limited",
    "ticker": "GEOJITFSL",
    "yf": "GEOJITFSL.NS"
  },
  {
    "name": "The Great Eastern Shipping Company Limited",
    "ticker": "GESHIP",
    "yf": "GESHIP.NS"
  },
  {
    "name": "GFL Limited",
    "ticker": "GFLLIMITED",
    "yf": "GFLLIMITED.NS"
  },
  {
    "name": "GHCL Limited",
    "ticker": "GHCL",
    "yf": "GHCL.NS"
  },
  {
    "name": "GHCL Textiles Limited",
    "ticker": "GHCLTEXTIL",
    "yf": "GHCLTEXTIL.NS"
  },
  {
    "name": "GIC Housing Finance Limited",
    "ticker": "GICHSGFIN",
    "yf": "GICHSGFIN.NS"
  },
  {
    "name": "Globe International Carriers Limited",
    "ticker": "GICL",
    "yf": "GICL.NS"
  },
  {
    "name": "General Insurance Corporation of India",
    "ticker": "GICRE",
    "yf": "GICRE.NS"
  },
  {
    "name": "Gillanders Arbuthnot & Company Limited",
    "ticker": "GILLANDERS",
    "yf": "GILLANDERS.NS"
  },
  {
    "name": "Gillette India Limited",
    "ticker": "GILLETTE",
    "yf": "GILLETTE.NS"
  },
  {
    "name": "Ginni Filaments Limited",
    "ticker": "GINNIFILA",
    "yf": "GINNIFILA.NS"
  },
  {
    "name": "Gujarat Industries Power Company Limited",
    "ticker": "GIPCL",
    "yf": "GIPCL.NS"
  },
  {
    "name": "GK Energy Limited",
    "ticker": "GKENERGY",
    "yf": "GKENERGY.NS"
  },
  {
    "name": "Gujarat Kidney And Super Speciality Limited",
    "ticker": "GKSL",
    "yf": "GKSL.NS"
  },
  {
    "name": "GKW Limited",
    "ticker": "GKWLIMITED",
    "yf": "GKWLIMITED.NS"
  },
  {
    "name": "Gland Pharma Limited",
    "ticker": "GLAND",
    "yf": "GLAND.NS"
  },
  {
    "name": "GlaxoSmithKline Pharmaceuticals Limited",
    "ticker": "GLAXO",
    "yf": "GLAXO.NS"
  },
  {
    "name": "Glenmark Pharmaceuticals Limited",
    "ticker": "GLENMARK",
    "yf": "GLENMARK.NS"
  },
  {
    "name": "Global Education Limited",
    "ticker": "GLOBAL",
    "yf": "GLOBAL.NS"
  },
  {
    "name": "Global Vectra Helicorp Limited",
    "ticker": "GLOBALVECT",
    "yf": "GLOBALVECT.NS"
  },
  {
    "name": "GLOBE ENTERPRISES (INDIA) LIMITED",
    "ticker": "GLOBE",
    "yf": "GLOBE.NS"
  },
  {
    "name": "Globus Spirits Limited",
    "ticker": "GLOBUSSPR",
    "yf": "GLOBUSSPR.NS"
  },
  {
    "name": "Gloster Limited",
    "ticker": "GLOSTERLTD",
    "yf": "GLOSTERLTD.NS"
  },
  {
    "name": "Glottis Limited",
    "ticker": "GLOTTIS",
    "yf": "GLOTTIS.NS"
  },
  {
    "name": "GM Breweries Limited",
    "ticker": "GMBREW",
    "yf": "GMBREW.NS"
  },
  {
    "name": "Gujarat Mineral Development Corporation Limited",
    "ticker": "GMDCLTD",
    "yf": "GMDCLTD.NS"
  },
  {
    "name": "GMM Pfaudler Limited",
    "ticker": "GMMPFAUDLR",
    "yf": "GMMPFAUDLR.NS"
  },
  {
    "name": "GMR AIRPORTS LIMITED",
    "ticker": "GMRAIRPORT",
    "yf": "GMRAIRPORT.NS"
  },
  {
    "name": "GMR Power and Urban Infra Limited",
    "ticker": "GMRP&UI",
    "yf": "GMRP&UI.NS"
  },
  {
    "name": "GNA Axles Limited",
    "ticker": "GNA",
    "yf": "GNA.NS"
  },
  {
    "name": "Gujarat Narmada Valley Fertilizers and Chemicals Limited",
    "ticker": "GNFC",
    "yf": "GNFC.NS"
  },
  {
    "name": "Gujarat Natural Resources Limited",
    "ticker": "GNRL",
    "yf": "GNRL.NS"
  },
  {
    "name": "Goa Carbon Limited",
    "ticker": "GOACARBON",
    "yf": "GOACARBON.NS"
  },
  {
    "name": "GOCL Corporation Limited",
    "ticker": "GOCLCORP",
    "yf": "GOCLCORP.NS"
  },
  {
    "name": "Go Fashion (India) Limited",
    "ticker": "GOCOLORS",
    "yf": "GOCOLORS.NS"
  },
  {
    "name": "Godavari Biorefineries Limited",
    "ticker": "GODAVARIB",
    "yf": "GODAVARIB.NS"
  },
  {
    "name": "Godfrey Phillips India Limited",
    "ticker": "GODFRYPHLP",
    "yf": "GODFRYPHLP.NS"
  },
  {
    "name": "Go Digit General Insurance Limited",
    "ticker": "GODIGIT",
    "yf": "GODIGIT.NS"
  },
  {
    "name": "Godrej Agrovet Limited",
    "ticker": "GODREJAGRO",
    "yf": "GODREJAGRO.NS"
  },
  {
    "name": "Godrej Consumer Products Limited",
    "ticker": "GODREJCP",
    "yf": "GODREJCP.NS"
  },
  {
    "name": "Godrej Industries Limited",
    "ticker": "GODREJIND",
    "yf": "GODREJIND.NS"
  },
  {
    "name": "Godrej Properties Limited",
    "ticker": "GODREJPROP",
    "yf": "GODREJPROP.NS"
  },
  {
    "name": "Gokaldas Exports Limited",
    "ticker": "GOKEX",
    "yf": "GOKEX.NS"
  },
  {
    "name": "Gokul Refoils and Solvent Limited",
    "ticker": "GOKUL",
    "yf": "GOKUL.NS"
  },
  {
    "name": "Gokul Agro Resources Limited",
    "ticker": "GOKULAGRO",
    "yf": "GOKULAGRO.NS"
  },
  {
    "name": "Goldiam International Limited",
    "ticker": "GOLDIAM",
    "yf": "GOLDIAM.NS"
  },
  {
    "name": "AION-TECH SOLUTIONS LIMITED",
    "ticker": "GOLDTECH",
    "yf": "GOLDTECH.NS"
  },
  {
    "name": "Goodluck India Limited",
    "ticker": "GOODLUCK",
    "yf": "GOODLUCK.NS"
  },
  {
    "name": "Goodyear India Limited",
    "ticker": "GOODYEAR",
    "yf": "GOODYEAR.NS"
  },
  {
    "name": "Gopal Snacks Limited",
    "ticker": "GOPAL",
    "yf": "GOPAL.NS"
  },
  {
    "name": "Goyal Aluminiums Limited",
    "ticker": "GOYALALUM",
    "yf": "GOYALALUM.NS"
  },
  {
    "name": "Godawari Power And Ispat limited",
    "ticker": "GPIL",
    "yf": "GPIL.NS"
  },
  {
    "name": "Gujarat Pipavav Port Limited",
    "ticker": "GPPL",
    "yf": "GPPL.NS"
  },
  {
    "name": "GPT Healthcare Limited",
    "ticker": "GPTHEALTH",
    "yf": "GPTHEALTH.NS"
  },
  {
    "name": "GPT Infraprojects Limited",
    "ticker": "GPTINFRA",
    "yf": "GPTINFRA.NS"
  },
  {
    "name": "Grand Oak Canyons Distillery Limited",
    "ticker": "GRANDOAK",
    "yf": "GRANDOAK.NS"
  },
  {
    "name": "Granules India Limited",
    "ticker": "GRANULES",
    "yf": "GRANULES.NS"
  },
  {
    "name": "Graphite India Limited",
    "ticker": "GRAPHITE",
    "yf": "GRAPHITE.NS"
  },
  {
    "name": "Grasim Industries Limited",
    "ticker": "GRASIM",
    "yf": "GRASIM.NS"
  },
  {
    "name": "Grauer & Weil India Limited",
    "ticker": "GRAUWEIL",
    "yf": "GRAUWEIL.NS"
  },
  {
    "name": "Graviss Hospitality Limited",
    "ticker": "GRAVISSHO",
    "yf": "GRAVISSHO.NS"
  },
  {
    "name": "Gravita India Limited",
    "ticker": "GRAVITA",
    "yf": "GRAVITA.NS"
  },
  {
    "name": "Greaves Cotton Limited",
    "ticker": "GREAVESCOT",
    "yf": "GREAVESCOT.NS"
  },
  {
    "name": "Greenlam Industries Limited",
    "ticker": "GREENLAM",
    "yf": "GREENLAM.NS"
  },
  {
    "name": "Greenpanel Industries Limited",
    "ticker": "GREENPANEL",
    "yf": "GREENPANEL.NS"
  },
  {
    "name": "Greenply Industries Limited",
    "ticker": "GREENPLY",
    "yf": "GREENPLY.NS"
  },
  {
    "name": "Orient Green Power Company Limited",
    "ticker": "GREENPOWER",
    "yf": "GREENPOWER.NS"
  },
  {
    "name": "Grindwell Norton Limited",
    "ticker": "GRINDWELL",
    "yf": "GRINDWELL.NS"
  },
  {
    "name": "G R Infraprojects Limited",
    "ticker": "GRINFRA",
    "yf": "GRINFRA.NS"
  },
  {
    "name": "GRM Overseas Limited",
    "ticker": "GRMOVER",
    "yf": "GRMOVER.NS"
  },
  {
    "name": "The Grob Tea Company Limited",
    "ticker": "GROBTEA",
    "yf": "GROBTEA.NS"
  },
  {
    "name": "Billionbrains Garage Ventures Limited",
    "ticker": "GROWW",
    "yf": "GROWW.NS"
  },
  {
    "name": "GRP Limited",
    "ticker": "GRPLTD",
    "yf": "GRPLTD.NS"
  },
  {
    "name": "Garden Reach Shipbuilders & Engineers Limited",
    "ticker": "GRSE",
    "yf": "GRSE.NS"
  },
  {
    "name": "Garware Hi-Tech Films Limited",
    "ticker": "GRWRHITECH",
    "yf": "GRWRHITECH.NS"
  },
  {
    "name": "Gujarat State Fertilizers & Chemicals Limited",
    "ticker": "GSFC",
    "yf": "GSFC.NS"
  },
  {
    "name": "Global Surfaces Limited",
    "ticker": "GSLSU",
    "yf": "GSLSU.NS"
  },
  {
    "name": "GSP Crop Science Limited",
    "ticker": "GSPCROP",
    "yf": "GSPCROP.NS"
  },
  {
    "name": "Gujarat State Petronet Limited",
    "ticker": "GSPL",
    "yf": "GSPL.NS"
  },
  {
    "name": "G-TEC JAINX EDUCATION LIMITED",
    "ticker": "GTECJAINX",
    "yf": "GTECJAINX.NS"
  },
  {
    "name": "GTL Infrastructure Limited",
    "ticker": "GTLINFRA",
    "yf": "GTLINFRA.NS"
  },
  {
    "name": "GTPL Hathway Limited",
    "ticker": "GTPL",
    "yf": "GTPL.NS"
  },
  {
    "name": "Gufic Biosciences Limited",
    "ticker": "GUFICBIO",
    "yf": "GUFICBIO.NS"
  },
  {
    "name": "Gujarat Alkalies and Chemicals Limited",
    "ticker": "GUJALKALI",
    "yf": "GUJALKALI.NS"
  },
  {
    "name": "Gujarat Apollo Industries Limited",
    "ticker": "GUJAPOLLO",
    "yf": "GUJAPOLLO.NS"
  },
  {
    "name": "Gujarat Gas Limited",
    "ticker": "GUJGASLTD",
    "yf": "GUJGASLTD.NS"
  },
  {
    "name": "Gujarat Raffia Industries Limited",
    "ticker": "GUJRAFFIA",
    "yf": "GUJRAFFIA.NS"
  },
  {
    "name": "Gujarat Themis Biosyn Limited",
    "ticker": "GUJTHEM",
    "yf": "GUJTHEM.NS"
  },
  {
    "name": "Gulf Oil Lubricants India Limited",
    "ticker": "GULFOILLUB",
    "yf": "GULFOILLUB.NS"
  },
  {
    "name": "GP Petroleums Limited",
    "ticker": "GULFPETRO",
    "yf": "GULFPETRO.NS"
  },
  {
    "name": "Gulshan Polyols Limited",
    "ticker": "GULPOLY",
    "yf": "GULPOLY.NS"
  },
  {
    "name": "GVP Infotech Limited",
    "ticker": "GVPTECH",
    "yf": "GVPTECH.NS"
  },
  {
    "name": "GE Vernova T&D India Limited",
    "ticker": "GVT&D",
    "yf": "GVT&D.NS"
  },
  {
    "name": "Hindustan Aeronautics Limited",
    "ticker": "HAL",
    "yf": "HAL.NS"
  },
  {
    "name": "Halder Venture Limited",
    "ticker": "HALDER",
    "yf": "HALDER.NS"
  },
  {
    "name": "Haldyn Glass Limited",
    "ticker": "HALDYNGL",
    "yf": "HALDYNGL.NS"
  },
  {
    "name": "HALEOS LABS LIMITED",
    "ticker": "HALEOSLABS",
    "yf": "HALEOSLABS.NS"
  },
  {
    "name": "Happiest Minds Technologies Limited",
    "ticker": "HAPPSTMNDS",
    "yf": "HAPPSTMNDS.NS"
  },
  {
    "name": "Happy Forgings Limited",
    "ticker": "HAPPYFORGE",
    "yf": "HAPPYFORGE.NS"
  },
  {
    "name": "Hardwyn India Limited",
    "ticker": "HARDWYN",
    "yf": "HARDWYN.NS"
  },
  {
    "name": "Hariom Pipe Industries Limited",
    "ticker": "HARIOMPIPE",
    "yf": "HARIOMPIPE.NS"
  },
  {
    "name": "Harrisons  Malayalam Limited",
    "ticker": "HARRMALAYA",
    "yf": "HARRMALAYA.NS"
  },
  {
    "name": "Harsha Engineers International Limited",
    "ticker": "HARSHA",
    "yf": "HARSHA.NS"
  },
  {
    "name": "Hathway Cable & Datacom Limited",
    "ticker": "HATHWAY",
    "yf": "HATHWAY.NS"
  },
  {
    "name": "Hatsun Agro Product Limited",
    "ticker": "HATSUN",
    "yf": "HATSUN.NS"
  },
  {
    "name": "Havells India Limited",
    "ticker": "HAVELLS",
    "yf": "HAVELLS.NS"
  },
  {
    "name": "Hawkins Cookers Limited",
    "ticker": "HAWKINCOOK",
    "yf": "HAWKINCOOK.NS"
  },
  {
    "name": "HB Estate Developers Limited",
    "ticker": "HBESD",
    "yf": "HBESD.NS"
  },
  {
    "name": "HBL Engineering Limited",
    "ticker": "HBLENGINE",
    "yf": "HBLENGINE.NS"
  },
  {
    "name": "Hindustan Construction Company Limited",
    "ticker": "HCC",
    "yf": "HCC.NS"
  },
  {
    "name": "Healthcare Global Enterprises Limited",
    "ticker": "HCG",
    "yf": "HCG.NS"
  },
  {
    "name": "HCL Infosystems Limited",
    "ticker": "HCL-INSYS",
    "yf": "HCL-INSYS.NS"
  },
  {
    "name": "HCL Technologies Limited",
    "ticker": "HCLTECH",
    "yf": "HCLTECH.NS"
  },
  {
    "name": "HDB Financial Services Limited",
    "ticker": "HDBFS",
    "yf": "HDBFS.NS"
  },
  {
    "name": "HDFC Asset Management Company Limited",
    "ticker": "HDFCAMC",
    "yf": "HDFCAMC.NS"
  },
  {
    "name": "HDFC Bank Limited",
    "ticker": "HDFCBANK",
    "yf": "HDFCBANK.NS"
  },
  {
    "name": "HDFC Life Insurance Company Limited",
    "ticker": "HDFCLIFE",
    "yf": "HDFCLIFE.NS"
  },
  {
    "name": "Heads UP Ventures Limited",
    "ticker": "HEADSUP",
    "yf": "HEADSUP.NS"
  },
  {
    "name": "Health X Platform Limited",
    "ticker": "HEALTHX",
    "yf": "HEALTHX.NS"
  },
  {
    "name": "HEC Infra Projects Limited",
    "ticker": "HECPROJECT",
    "yf": "HECPROJECT.NS"
  },
  {
    "name": "HEG Limited",
    "ticker": "HEG",
    "yf": "HEG.NS"
  },
  {
    "name": "HeidelbergCement India Limited",
    "ticker": "HEIDELBERG",
    "yf": "HEIDELBERG.NS"
  },
  {
    "name": "Hemisphere Properties India Limited",
    "ticker": "HEMIPROP",
    "yf": "HEMIPROP.NS"
  },
  {
    "name": "Heranba Industries Limited",
    "ticker": "HERANBA",
    "yf": "HERANBA.NS"
  },
  {
    "name": "Heritage Foods Limited",
    "ticker": "HERITGFOOD",
    "yf": "HERITGFOOD.NS"
  },
  {
    "name": "Hero MotoCorp Limited",
    "ticker": "HEROMOTOCO",
    "yf": "HEROMOTOCO.NS"
  },
  {
    "name": "Hester Biosciences Limited",
    "ticker": "HESTERBIO",
    "yf": "HESTERBIO.NS"
  },
  {
    "name": "Hexa Tradex Limited",
    "ticker": "HEXATRADEX",
    "yf": "HEXATRADEX.NS"
  },
  {
    "name": "Hexaware Technologies Limited",
    "ticker": "HEXT",
    "yf": "HEXT.NS"
  },
  {
    "name": "HFCL Limited",
    "ticker": "HFCL",
    "yf": "HFCL.NS"
  },
  {
    "name": "H.G. Infra Engineering Limited",
    "ticker": "HGINFRA",
    "yf": "HGINFRA.NS"
  },
  {
    "name": "HandsOn Global Management (HGM) Limited",
    "ticker": "HGM",
    "yf": "HGM.NS"
  },
  {
    "name": "Hinduja Global Solutions Limited",
    "ticker": "HGS",
    "yf": "HGS.NS"
  },
  {
    "name": "Hikal Limited",
    "ticker": "HIKAL",
    "yf": "HIKAL.NS"
  },
  {
    "name": "Hilton Metal Forging Limited",
    "ticker": "HILTON",
    "yf": "HILTON.NS"
  },
  {
    "name": "Himatsingka Seide Limited",
    "ticker": "HIMATSEIDE",
    "yf": "HIMATSEIDE.NS"
  },
  {
    "name": "Hindalco Industries Limited",
    "ticker": "HINDALCO",
    "yf": "HINDALCO.NS"
  },
  {
    "name": "Hindustan Composites Limited",
    "ticker": "HINDCOMPOS",
    "yf": "HINDCOMPOS.NS"
  },
  {
    "name": "Hindustan Copper Limited",
    "ticker": "HINDCOPPER",
    "yf": "HINDCOPPER.NS"
  },
  {
    "name": "Hindustan Oil Exploration Company Limited",
    "ticker": "HINDOILEXP",
    "yf": "HINDOILEXP.NS"
  },
  {
    "name": "Hindustan Petroleum Corporation Limited",
    "ticker": "HINDPETRO",
    "yf": "HINDPETRO.NS"
  },
  {
    "name": "Hindustan Unilever Limited",
    "ticker": "HINDUNILVR",
    "yf": "HINDUNILVR.NS"
  },
  {
    "name": "Hindware Home Innovation Limited",
    "ticker": "HINDWAREAP",
    "yf": "HINDWAREAP.NS"
  },
  {
    "name": "Hindustan Zinc Limited",
    "ticker": "HINDZINC",
    "yf": "HINDZINC.NS"
  },
  {
    "name": "Hind Rectifiers Limited",
    "ticker": "HIRECT",
    "yf": "HIRECT.NS"
  },
  {
    "name": "Hisar Metal Industries Limited",
    "ticker": "HISARMETAL",
    "yf": "HISARMETAL.NS"
  },
  {
    "name": "Hi-Tech Pipes Limited",
    "ticker": "HITECH",
    "yf": "HITECH.NS"
  },
  {
    "name": "Hitech Corporation Limited",
    "ticker": "HITECHCORP",
    "yf": "HITECHCORP.NS"
  },
  {
    "name": "HLE Glascoat Limited",
    "ticker": "HLEGLAS",
    "yf": "HLEGLAS.NS"
  },
  {
    "name": "HLV LIMITED",
    "ticker": "HLVLTD",
    "yf": "HLVLTD.NS"
  },
  {
    "name": "HMA Agro Industries Limited",
    "ticker": "HMAAGRO",
    "yf": "HMAAGRO.NS"
  },
  {
    "name": "Hindustan Media Ventures Limited",
    "ticker": "HMVL",
    "yf": "HMVL.NS"
  },
  {
    "name": "Hindustan Foods Limited",
    "ticker": "HNDFDS",
    "yf": "HNDFDS.NS"
  },
  {
    "name": "Home First Finance Company India Limited",
    "ticker": "HOMEFIRST",
    "yf": "HOMEFIRST.NS"
  },
  {
    "name": "Honasa Consumer Limited",
    "ticker": "HONASA",
    "yf": "HONASA.NS"
  },
  {
    "name": "Honeywell Automation India Limited",
    "ticker": "HONAUT",
    "yf": "HONAUT.NS"
  },
  {
    "name": "Honda India Power Products Limited",
    "ticker": "HONDAPOWER",
    "yf": "HONDAPOWER.NS"
  },
  {
    "name": "HP Adhesives Limited",
    "ticker": "HPAL",
    "yf": "HPAL.NS"
  },
  {
    "name": "Hindprakash Industries Limited",
    "ticker": "HPIL",
    "yf": "HPIL.NS"
  },
  {
    "name": "HPL Electric & Power Limited",
    "ticker": "HPL",
    "yf": "HPL.NS"
  },
  {
    "name": "Himadri Speciality Chemical Limited",
    "ticker": "HSCL",
    "yf": "HSCL.NS"
  },
  {
    "name": "HT Media Limited",
    "ticker": "HTMEDIA",
    "yf": "HTMEDIA.NS"
  },
  {
    "name": "Hubtown Limited",
    "ticker": "HUBTOWN",
    "yf": "HUBTOWN.NS"
  },
  {
    "name": "Housing & Urban Development Corporation Limited",
    "ticker": "HUDCO",
    "yf": "HUDCO.NS"
  },
  {
    "name": "Huhtamaki India Limited",
    "ticker": "HUHTAMAKI",
    "yf": "HUHTAMAKI.NS"
  },
  {
    "name": "Hybrid Financial Services Limited",
    "ticker": "HYBRIDFIN",
    "yf": "HYBRIDFIN.NS"
  },
  {
    "name": "Hyundai Motor India Limited",
    "ticker": "HYUNDAI",
    "yf": "HYUNDAI.NS"
  },
  {
    "name": "Indiabulls Limited",
    "ticker": "IBULLSLTD",
    "yf": "IBULLSLTD.NS"
  },
  {
    "name": "Ice Make Refrigeration Limited",
    "ticker": "ICEMAKE",
    "yf": "ICEMAKE.NS"
  },
  {
    "name": "ICICI Prudential Asset Management Company Limited",
    "ticker": "ICICIAMC",
    "yf": "ICICIAMC.NS"
  },
  {
    "name": "ICICI Bank Limited",
    "ticker": "ICICIBANK",
    "yf": "ICICIBANK.NS"
  },
  {
    "name": "ICICI Lombard General Insurance Company Limited",
    "ticker": "ICICIGI",
    "yf": "ICICIGI.NS"
  },
  {
    "name": "ICICI Prudential Life Insurance Company Limited",
    "ticker": "ICICIPRULI",
    "yf": "ICICIPRULI.NS"
  },
  {
    "name": "Indo Count Industries Limited",
    "ticker": "ICIL",
    "yf": "ICIL.NS"
  },
  {
    "name": "ICRA Limited",
    "ticker": "ICRA",
    "yf": "ICRA.NS"
  },
  {
    "name": "IDBI Bank Limited",
    "ticker": "IDBI",
    "yf": "IDBI.NS"
  },
  {
    "name": "Vodafone Idea Limited",
    "ticker": "IDEA",
    "yf": "IDEA.NS"
  },
  {
    "name": "Ideaforge Technology Limited",
    "ticker": "IDEAFORGE",
    "yf": "IDEAFORGE.NS"
  },
  {
    "name": "IDFC First Bank Limited",
    "ticker": "IDFCFIRSTB",
    "yf": "IDFCFIRSTB.NS"
  },
  {
    "name": "Indian Energy Exchange Limited",
    "ticker": "IEX",
    "yf": "IEX.NS"
  },
  {
    "name": "IFB Agro Industries Limited",
    "ticker": "IFBAGRO",
    "yf": "IFBAGRO.NS"
  },
  {
    "name": "IFB Industries Limited",
    "ticker": "IFBIND",
    "yf": "IFBIND.NS"
  },
  {
    "name": "IFCI Limited",
    "ticker": "IFCI",
    "yf": "IFCI.NS"
  },
  {
    "name": "IFGL Refractories Limited",
    "ticker": "IFGLEXPOR",
    "yf": "IFGLEXPOR.NS"
  },
  {
    "name": "Igarashi Motors India Limited",
    "ticker": "IGARASHI",
    "yf": "IGARASHI.NS"
  },
  {
    "name": "Indogulf Cropsciences Limited",
    "ticker": "IGCL",
    "yf": "IGCL.NS"
  },
  {
    "name": "International Gemmological Institute (India) Limited",
    "ticker": "IGIL",
    "yf": "IGIL.NS"
  },
  {
    "name": "Indraprastha Gas Limited",
    "ticker": "IGL",
    "yf": "IGL.NS"
  },
  {
    "name": "IG Petrochemicals Limited",
    "ticker": "IGPL",
    "yf": "IGPL.NS"
  },
  {
    "name": "IIFL Finance Limited",
    "ticker": "IIFL",
    "yf": "IIFL.NS"
  },
  {
    "name": "IIFL Capital Services Limited",
    "ticker": "IIFLCAPS",
    "yf": "IIFLCAPS.NS"
  },
  {
    "name": "Industrial Investment Trust Limited",
    "ticker": "IITL",
    "yf": "IITL.NS"
  },
  {
    "name": "IKIO Technologies Limited",
    "ticker": "IKIO",
    "yf": "IKIO.NS"
  },
  {
    "name": "Inventurus Knowledge Solutions Limited",
    "ticker": "IKS",
    "yf": "IKS.NS"
  },
  {
    "name": "Imagicaaworld Entertainment Limited",
    "ticker": "IMAGICAA",
    "yf": "IMAGICAA.NS"
  },
  {
    "name": "Indian Metals & Ferro Alloys Limited",
    "ticker": "IMFA",
    "yf": "IMFA.NS"
  },
  {
    "name": "India Motor Parts and Accessories Limited",
    "ticker": "IMPAL",
    "yf": "IMPAL.NS"
  },
  {
    "name": "Insolation Energy Limited",
    "ticker": "INA",
    "yf": "INA.NS"
  },
  {
    "name": "INCREDIBLE INDUSTRIES LIMITED",
    "ticker": "INCREDIBLE",
    "yf": "INCREDIBLE.NS"
  },
  {
    "name": "Indbank Merchant Banking Services Limited",
    "ticker": "INDBANK",
    "yf": "INDBANK.NS"
  },
  {
    "name": "Indegene Limited",
    "ticker": "INDGN",
    "yf": "INDGN.NS"
  },
  {
    "name": "The Indian Hotels Company Limited",
    "ticker": "INDHOTEL",
    "yf": "INDHOTEL.NS"
  },
  {
    "name": "The India Cements Limited",
    "ticker": "INDIACEM",
    "yf": "INDIACEM.NS"
  },
  {
    "name": "India Glycols Limited",
    "ticker": "INDIAGLYCO",
    "yf": "INDIAGLYCO.NS"
  },
  {
    "name": "Indiamart Intermesh Limited",
    "ticker": "INDIAMART",
    "yf": "INDIAMART.NS"
  },
  {
    "name": "Indian Bank",
    "ticker": "INDIANB",
    "yf": "INDIANB.NS"
  },
  {
    "name": "Indian Card Clothing Company Limited",
    "ticker": "INDIANCARD",
    "yf": "INDIANCARD.NS"
  },
  {
    "name": "Indian Hume Pipe Company Limited",
    "ticker": "INDIANHUME",
    "yf": "INDIANHUME.NS"
  },
  {
    "name": "India Shelter Finance Corporation Limited",
    "ticker": "INDIASHLTR",
    "yf": "INDIASHLTR.NS"
  },
  {
    "name": "InterGlobe Aviation Limited",
    "ticker": "INDIGO",
    "yf": "INDIGO.NS"
  },
  {
    "name": "Indigo Paints Limited",
    "ticker": "INDIGOPNTS",
    "yf": "INDIGOPNTS.NS"
  },
  {
    "name": "Indiqube Spaces Limited",
    "ticker": "INDIQUBE",
    "yf": "INDIQUBE.NS"
  },
  {
    "name": "India Nippon Electricals Limited",
    "ticker": "INDNIPPON",
    "yf": "INDNIPPON.NS"
  },
  {
    "name": "Indo Amines Limited",
    "ticker": "INDOAMIN",
    "yf": "INDOAMIN.NS"
  },
  {
    "name": "Indo Borax & Chemicals Limited",
    "ticker": "INDOBORAX",
    "yf": "INDOBORAX.NS"
  },
  {
    "name": "Indoco Remedies Limited",
    "ticker": "INDOCO",
    "yf": "INDOCO.NS"
  },
  {
    "name": "Indo Farm Equipment Limited",
    "ticker": "INDOFARM",
    "yf": "INDOFARM.NS"
  },
  {
    "name": "Indo Rama Synthetics (India) Limited",
    "ticker": "INDORAMA",
    "yf": "INDORAMA.NS"
  },
  {
    "name": "IndoStar Capital Finance Limited",
    "ticker": "INDOSTAR",
    "yf": "INDOSTAR.NS"
  },
  {
    "name": "Indo Tech Transformers Limited",
    "ticker": "INDOTECH",
    "yf": "INDOTECH.NS"
  },
  {
    "name": "Indo Thai Securities Limited",
    "ticker": "INDOTHAI",
    "yf": "INDOTHAI.NS"
  },
  {
    "name": "Indo Us Biotech Limited",
    "ticker": "INDOUS",
    "yf": "INDOUS.NS"
  },
  {
    "name": "Indowind Energy Limited",
    "ticker": "INDOWIND",
    "yf": "INDOWIND.NS"
  },
  {
    "name": "Industrial & Prudential Investment Company Limited",
    "ticker": "INDPRUD",
    "yf": "INDPRUD.NS"
  },
  {
    "name": "Indraprastha Medical Corporation Limited",
    "ticker": "INDRAMEDCO",
    "yf": "INDRAMEDCO.NS"
  },
  {
    "name": "Ind-Swift Laboratories Limited",
    "ticker": "INDSWFTLAB",
    "yf": "INDSWFTLAB.NS"
  },
  {
    "name": "Indian Terrain Fashions Limited",
    "ticker": "INDTERRAIN",
    "yf": "INDTERRAIN.NS"
  },
  {
    "name": "IndusInd Bank Limited",
    "ticker": "INDUSINDBK",
    "yf": "INDUSINDBK.NS"
  },
  {
    "name": "Indus Towers Limited",
    "ticker": "INDUSTOWER",
    "yf": "INDUSTOWER.NS"
  },
  {
    "name": "InfoBeans Technologies Limited",
    "ticker": "INFOBEAN",
    "yf": "INFOBEAN.NS"
  },
  {
    "name": "Infomedia Press Limited",
    "ticker": "INFOMEDIA",
    "yf": "INFOMEDIA.NS"
  },
  {
    "name": "Infosys Limited",
    "ticker": "INFY",
    "yf": "INFY.NS"
  },
  {
    "name": "Ingersoll Rand (India) Limited",
    "ticker": "INGERRAND",
    "yf": "INGERRAND.NS"
  },
  {
    "name": "Innova Captab Limited",
    "ticker": "INNOVACAP",
    "yf": "INNOVACAP.NS"
  },
  {
    "name": "Innovana Thinklabs Limited",
    "ticker": "INNOVANA",
    "yf": "INNOVANA.NS"
  },
  {
    "name": "Innovision Limited",
    "ticker": "INNOVISION",
    "yf": "INNOVISION.NS"
  },
  {
    "name": "Inox Green Energy Services Limited",
    "ticker": "INOXGREEN",
    "yf": "INOXGREEN.NS"
  },
  {
    "name": "INOX India Limited",
    "ticker": "INOXINDIA",
    "yf": "INOXINDIA.NS"
  },
  {
    "name": "Inox Wind Limited",
    "ticker": "INOXWIND",
    "yf": "INOXWIND.NS"
  },
  {
    "name": "Insecticides (India) Limited",
    "ticker": "INSECTICID",
    "yf": "INSECTICID.NS"
  },
  {
    "name": "Intellect Design Arena Limited",
    "ticker": "INTELLECT",
    "yf": "INTELLECT.NS"
  },
  {
    "name": "Intense Technologies Limited",
    "ticker": "INTENTECH",
    "yf": "INTENTECH.NS"
  },
  {
    "name": "Interarch Building Solutions Limited",
    "ticker": "INTERARCH",
    "yf": "INTERARCH.NS"
  },
  {
    "name": "International Conveyors Limited",
    "ticker": "INTLCONV",
    "yf": "INTLCONV.NS"
  },
  {
    "name": "Inventure Growth & Securities Limited",
    "ticker": "INVENTURE",
    "yf": "INVENTURE.NS"
  },
  {
    "name": "Investment & Precision Castings Limited",
    "ticker": "INVPRECQ",
    "yf": "INVPRECQ.NS"
  },
  {
    "name": "Indian Overseas Bank",
    "ticker": "IOB",
    "yf": "IOB.NS"
  },
  {
    "name": "Indian Oil Corporation Limited",
    "ticker": "IOC",
    "yf": "IOC.NS"
  },
  {
    "name": "IOL Chemicals and Pharmaceuticals Limited",
    "ticker": "IOLCP",
    "yf": "IOLCP.NS"
  },
  {
    "name": "ION Exchange (India) Limited",
    "ticker": "IONEXCHANG",
    "yf": "IONEXCHANG.NS"
  },
  {
    "name": "IPCA Laboratories Limited",
    "ticker": "IPCALAB",
    "yf": "IPCALAB.NS"
  },
  {
    "name": "India Pesticides Limited",
    "ticker": "IPL",
    "yf": "IPL.NS"
  },
  {
    "name": "IRB Infrastructure Developers Limited",
    "ticker": "IRB",
    "yf": "IRB.NS"
  },
  {
    "name": "Ircon International Limited",
    "ticker": "IRCON",
    "yf": "IRCON.NS"
  },
  {
    "name": "Indian Railway Catering And Tourism Corporation Limited",
    "ticker": "IRCTC",
    "yf": "IRCTC.NS"
  },
  {
    "name": "Indian Renewable Energy Development Agency Limited",
    "ticker": "IREDA",
    "yf": "IREDA.NS"
  },
  {
    "name": "Indian Railway Finance Corporation Limited",
    "ticker": "IRFC",
    "yf": "IRFC.NS"
  },
  {
    "name": "IRIS RegTech Solutions Limited",
    "ticker": "IRIS",
    "yf": "IRIS.NS"
  },
  {
    "name": "Iris Clothings Limited",
    "ticker": "IRISDOREME",
    "yf": "IRISDOREME.NS"
  },
  {
    "name": "IRM Energy Limited",
    "ticker": "IRMENERGY",
    "yf": "IRMENERGY.NS"
  },
  {
    "name": "Intrasoft Technologies Limited",
    "ticker": "ISFT",
    "yf": "ISFT.NS"
  },
  {
    "name": "Isgec Heavy Engineering Limited",
    "ticker": "ISGEC",
    "yf": "ISGEC.NS"
  },
  {
    "name": "Ishan Dyes and Chemicals Limited",
    "ticker": "ISHANCH",
    "yf": "ISHANCH.NS"
  },
  {
    "name": "ITC Limited",
    "ticker": "ITC",
    "yf": "ITC.NS"
  },
  {
    "name": "ITC Hotels Limited",
    "ticker": "ITCHOTELS",
    "yf": "ITCHOTELS.NS"
  },
  {
    "name": "India Tourism Development Corporation Limited",
    "ticker": "ITDC",
    "yf": "ITDC.NS"
  },
  {
    "name": "ITI Limited",
    "ticker": "ITI",
    "yf": "ITI.NS"
  },
  {
    "name": "Ivalue Infosolutions Limited",
    "ticker": "IVALUE",
    "yf": "IVALUE.NS"
  },
  {
    "name": "IL&FS Investment Managers Limited",
    "ticker": "IVC",
    "yf": "IVC.NS"
  },
  {
    "name": "IVP Limited",
    "ticker": "IVP",
    "yf": "IVP.NS"
  },
  {
    "name": "The Indian Wood Products Company Limited",
    "ticker": "IWP",
    "yf": "IWP.NS"
  },
  {
    "name": "Le Travenues Technology Limited",
    "ticker": "IXIGO",
    "yf": "IXIGO.NS"
  },
  {
    "name": "The Jammu & Kashmir Bank Limited",
    "ticker": "J&KBANK",
    "yf": "J&KBANK.NS"
  },
  {
    "name": "Jagran Prakashan Limited",
    "ticker": "JAGRAN",
    "yf": "JAGRAN.NS"
  },
  {
    "name": "Jagsonpal Pharmaceuticals Limited",
    "ticker": "JAGSNPHARM",
    "yf": "JAGSNPHARM.NS"
  },
  {
    "name": "Jai Balaji Industries Limited",
    "ticker": "JAIBALAJI",
    "yf": "JAIBALAJI.NS"
  },
  {
    "name": "Jai Corp Limited",
    "ticker": "JAICORPLTD",
    "yf": "JAICORPLTD.NS"
  },
  {
    "name": "Jain Resource Recycling Limited",
    "ticker": "JAINREC",
    "yf": "JAINREC.NS"
  },
  {
    "name": "Nandani Creation Limited",
    "ticker": "JAIPURKURT",
    "yf": "JAIPURKURT.NS"
  },
  {
    "name": "Jamna Auto Industries Limited",
    "ticker": "JAMNAAUTO",
    "yf": "JAMNAAUTO.NS"
  },
  {
    "name": "Jaro Institute of Technology Management and Research Limited",
    "ticker": "JARO",
    "yf": "JARO.NS"
  },
  {
    "name": "Jash Engineering Limited",
    "ticker": "JASH",
    "yf": "JASH.NS"
  },
  {
    "name": "Jayant Agro Organics Limited",
    "ticker": "JAYAGROGN",
    "yf": "JAYAGROGN.NS"
  },
  {
    "name": "Jay Bharat Maruti Limited",
    "ticker": "JAYBARMARU",
    "yf": "JAYBARMARU.NS"
  },
  {
    "name": "Jaykay Enterprises Limited",
    "ticker": "JAYKAY",
    "yf": "JAYKAY.NS"
  },
  {
    "name": "Jayaswal Neco Industries Limited",
    "ticker": "JAYNECOIND",
    "yf": "JAYNECOIND.NS"
  },
  {
    "name": "Jayshree Tea & Industries Limited",
    "ticker": "JAYSREETEA",
    "yf": "JAYSREETEA.NS"
  },
  {
    "name": "JB Chemicals & Pharmaceuticals Limited",
    "ticker": "JBCHEPHARM",
    "yf": "JBCHEPHARM.NS"
  },
  {
    "name": "JBM Auto Limited",
    "ticker": "JBMA",
    "yf": "JBMA.NS"
  },
  {
    "name": "Jet Freight Logistics Limited",
    "ticker": "JETFREIGHT",
    "yf": "JETFREIGHT.NS"
  },
  {
    "name": "J.G.Chemicals Limited",
    "ticker": "JGCHEM",
    "yf": "JGCHEM.NS"
  },
  {
    "name": "Jindal Photo Limited",
    "ticker": "JINDALPHOT",
    "yf": "JINDALPHOT.NS"
  },
  {
    "name": "Jindal Poly Films Limited",
    "ticker": "JINDALPOLY",
    "yf": "JINDALPOLY.NS"
  },
  {
    "name": "Jindal Saw Limited",
    "ticker": "JINDALSAW",
    "yf": "JINDALSAW.NS"
  },
  {
    "name": "JINDAL STEEL LIMITED",
    "ticker": "JINDALSTEL",
    "yf": "JINDALSTEL.NS"
  },
  {
    "name": "Jindal Drilling And Industries Limited",
    "ticker": "JINDRILL",
    "yf": "JINDRILL.NS"
  },
  {
    "name": "Jindal Worldwide Limited",
    "ticker": "JINDWORLD",
    "yf": "JINDWORLD.NS"
  },
  {
    "name": "Jio Financial Services Limited",
    "ticker": "JIOFIN",
    "yf": "JIOFIN.NS"
  },
  {
    "name": "Jain Irrigation Systems Limited",
    "ticker": "JISLDVREQS",
    "yf": "JISLDVREQS.NS"
  },
  {
    "name": "Jain Irrigation Systems Limited",
    "ticker": "JISLJALEQS",
    "yf": "JISLJALEQS.NS"
  },
  {
    "name": "JK Cement Limited",
    "ticker": "JKCEMENT",
    "yf": "JKCEMENT.NS"
  },
  {
    "name": "J.Kumar Infraprojects Limited",
    "ticker": "JKIL",
    "yf": "JKIL.NS"
  },
  {
    "name": "JK Lakshmi Cement Limited",
    "ticker": "JKLAKSHMI",
    "yf": "JKLAKSHMI.NS"
  },
  {
    "name": "JK Paper Limited",
    "ticker": "JKPAPER",
    "yf": "JKPAPER.NS"
  },
  {
    "name": "JK Tyre & Industries Limited",
    "ticker": "JKTYRE",
    "yf": "JKTYRE.NS"
  },
  {
    "name": "Jupiter Life Line Hospitals Limited",
    "ticker": "JLHL",
    "yf": "JLHL.NS"
  },
  {
    "name": "Jullundur Motor Agency (Delhi) Limited",
    "ticker": "JMA",
    "yf": "JMA.NS"
  },
  {
    "name": "JM Financial Limited",
    "ticker": "JMFINANCIL",
    "yf": "JMFINANCIL.NS"
  },
  {
    "name": "JNK India Limited",
    "ticker": "JNKINDIA",
    "yf": "JNKINDIA.NS"
  },
  {
    "name": "Jocil Limited",
    "ticker": "JOCIL",
    "yf": "JOCIL.NS"
  },
  {
    "name": "Jindal Poly Investment and Finance Company Limited",
    "ticker": "JPOLYINVST",
    "yf": "JPOLYINVST.NS"
  },
  {
    "name": "Jaiprakash Power Ventures Limited",
    "ticker": "JPPOWER",
    "yf": "JPPOWER.NS"
  },
  {
    "name": "Jana Small Finance Bank Limited",
    "ticker": "JSFB",
    "yf": "JSFB.NS"
  },
  {
    "name": "Jindal Stainless Limited",
    "ticker": "JSL",
    "yf": "JSL.NS"
  },
  {
    "name": "Jeena Sikho Lifecare Limited",
    "ticker": "JSLL",
    "yf": "JSLL.NS"
  },
  {
    "name": "JSW Cement Limited",
    "ticker": "JSWCEMENT",
    "yf": "JSWCEMENT.NS"
  },
  {
    "name": "JSW Dulux Limited",
    "ticker": "JSWDULUX",
    "yf": "JSWDULUX.NS"
  },
  {
    "name": "JSW Energy Limited",
    "ticker": "JSWENERGY",
    "yf": "JSWENERGY.NS"
  },
  {
    "name": "JSW Holdings Limited",
    "ticker": "JSWHL",
    "yf": "JSWHL.NS"
  },
  {
    "name": "JSW Infrastructure Limited",
    "ticker": "JSWINFRA",
    "yf": "JSWINFRA.NS"
  },
  {
    "name": "JSW Steel Limited",
    "ticker": "JSWSTEEL",
    "yf": "JSWSTEEL.NS"
  },
  {
    "name": "Jtekt India Limited",
    "ticker": "JTEKTINDIA",
    "yf": "JTEKTINDIA.NS"
  },
  {
    "name": "JTL INDUSTRIES LIMITED",
    "ticker": "JTLIND",
    "yf": "JTLIND.NS"
  },
  {
    "name": "Jubilant Agri and Consumer Products Limited",
    "ticker": "JUBLCPL",
    "yf": "JUBLCPL.NS"
  },
  {
    "name": "Jubilant Foodworks Limited",
    "ticker": "JUBLFOOD",
    "yf": "JUBLFOOD.NS"
  },
  {
    "name": "Jubilant Ingrevia Limited",
    "ticker": "JUBLINGREA",
    "yf": "JUBLINGREA.NS"
  },
  {
    "name": "Jubilant Pharmova Limited",
    "ticker": "JUBLPHARMA",
    "yf": "JUBLPHARMA.NS"
  },
  {
    "name": "Juniper Hotels Limited",
    "ticker": "JUNIPER",
    "yf": "JUNIPER.NS"
  },
  {
    "name": "Just Dial Limited",
    "ticker": "JUSTDIAL",
    "yf": "JUSTDIAL.NS"
  },
  {
    "name": "Jupiter Wagons Limited",
    "ticker": "JWL",
    "yf": "JWL.NS"
  },
  {
    "name": "Jyothy Labs Limited",
    "ticker": "JYOTHYLAB",
    "yf": "JYOTHYLAB.NS"
  },
  {
    "name": "Jyoti CNC Automation Limited",
    "ticker": "JYOTICNC",
    "yf": "JYOTICNC.NS"
  },
  {
    "name": "Jyoti Structures Limited",
    "ticker": "JYOTISTRUC",
    "yf": "JYOTISTRUC.NS"
  },
  {
    "name": "Kabra Extrusion Technik Limited",
    "ticker": "KABRAEXTRU",
    "yf": "KABRAEXTRU.NS"
  },
  {
    "name": "Kajaria Ceramics Limited",
    "ticker": "KAJARIACER",
    "yf": "KAJARIACER.NS"
  },
  {
    "name": "Sai Silks (Kalamandir) Limited",
    "ticker": "KALAMANDIR",
    "yf": "KALAMANDIR.NS"
  },
  {
    "name": "Kalpataru Limited",
    "ticker": "KALPATARU",
    "yf": "KALPATARU.NS"
  },
  {
    "name": "Kalyani Forge Limited",
    "ticker": "KALYANIFRG",
    "yf": "KALYANIFRG.NS"
  },
  {
    "name": "Kalyan Jewellers India Limited",
    "ticker": "KALYANKJIL",
    "yf": "KALYANKJIL.NS"
  },
  {
    "name": "Kama Holdings Limited",
    "ticker": "KAMAHOLD",
    "yf": "KAMAHOLD.NS"
  },
  {
    "name": "Kamat Hotels (I) Limited",
    "ticker": "KAMATHOTEL",
    "yf": "KAMATHOTEL.NS"
  },
  {
    "name": "Kamdhenu Limited",
    "ticker": "KAMDHENU",
    "yf": "KAMDHENU.NS"
  },
  {
    "name": "Kanani Industries Limited",
    "ticker": "KANANIIND",
    "yf": "KANANIIND.NS"
  },
  {
    "name": "Kanoria Chemicals & Industries Limited",
    "ticker": "KANORICHEM",
    "yf": "KANORICHEM.NS"
  },
  {
    "name": "Kanpur Plastipack Limited",
    "ticker": "KANPRPLA",
    "yf": "KANPRPLA.NS"
  },
  {
    "name": "Kansai Nerolac Paints Limited",
    "ticker": "KANSAINER",
    "yf": "KANSAINER.NS"
  },
  {
    "name": "Karma Energy Limited",
    "ticker": "KARMAENG",
    "yf": "KARMAENG.NS"
  },
  {
    "name": "Karur Vysya Bank Limited",
    "ticker": "KARURVYSYA",
    "yf": "KARURVYSYA.NS"
  },
  {
    "name": "Kaushalya Infrastructure Development Corporation Limited",
    "ticker": "KAUSHALYA",
    "yf": "KAUSHALYA.NS"
  },
  {
    "name": "Kaya Limited",
    "ticker": "KAYA",
    "yf": "KAYA.NS"
  },
  {
    "name": "Kaynes Technology India Limited",
    "ticker": "KAYNES",
    "yf": "KAYNES.NS"
  },
  {
    "name": "KCP Limited",
    "ticker": "KCP",
    "yf": "KCP.NS"
  },
  {
    "name": "KCP Sugar and Industries Corporation Limited",
    "ticker": "KCPSUGIND",
    "yf": "KCPSUGIND.NS"
  },
  {
    "name": "KDDL Limited",
    "ticker": "KDDL",
    "yf": "KDDL.NS"
  },
  {
    "name": "KEC International Limited",
    "ticker": "KEC",
    "yf": "KEC.NS"
  },
  {
    "name": "DSJ Keep Learning Limited",
    "ticker": "KEEPLEARN",
    "yf": "KEEPLEARN.NS"
  },
  {
    "name": "KEI Industries Limited",
    "ticker": "KEI",
    "yf": "KEI.NS"
  },
  {
    "name": "Kellton Tech Solutions Limited",
    "ticker": "KELLTONTEC",
    "yf": "KELLTONTEC.NS"
  },
  {
    "name": "Kennametal India Limited",
    "ticker": "KENNAMET",
    "yf": "KENNAMET.NS"
  },
  {
    "name": "Kernex Microsystems (India) Limited",
    "ticker": "KERNEX",
    "yf": "KERNEX.NS"
  },
  {
    "name": "Kesoram Industries Limited",
    "ticker": "KESORAMIND",
    "yf": "KESORAMIND.NS"
  },
  {
    "name": "Keynote Financial Services Limited",
    "ticker": "KEYFINSERV",
    "yf": "KEYFINSERV.NS"
  },
  {
    "name": "Kfin Technologies Limited",
    "ticker": "KFINTECH",
    "yf": "KFINTECH.NS"
  },
  {
    "name": "Khadim India Limited",
    "ticker": "KHADIM",
    "yf": "KHADIM.NS"
  },
  {
    "name": "Khandwala Securities Limited",
    "ticker": "KHANDSE",
    "yf": "KHANDSE.NS"
  },
  {
    "name": "Kalyani Investment Company Limited",
    "ticker": "KICL",
    "yf": "KICL.NS"
  },
  {
    "name": "Kilitch Drugs (India) Limited",
    "ticker": "KILITCH",
    "yf": "KILITCH.NS"
  },
  {
    "name": "Krishna Institute of Medical Sciences Limited",
    "ticker": "KIMS",
    "yf": "KIMS.NS"
  },
  {
    "name": "Kingfa Science & Technology (India) Limited",
    "ticker": "KINGFA",
    "yf": "KINGFA.NS"
  },
  {
    "name": "KIOCL Limited",
    "ticker": "KIOCL",
    "yf": "KIOCL.NS"
  },
  {
    "name": "Kiran Vyapar Limited",
    "ticker": "KIRANVYPAR",
    "yf": "KIRANVYPAR.NS"
  },
  {
    "name": "Kiri Industries Limited",
    "ticker": "KIRIINDUS",
    "yf": "KIRIINDUS.NS"
  },
  {
    "name": "Kirloskar Ferrous Industries Limited",
    "ticker": "KIRLFER",
    "yf": "KIRLFER.NS"
  },
  {
    "name": "Kirloskar Brothers Limited",
    "ticker": "KIRLOSBROS",
    "yf": "KIRLOSBROS.NS"
  },
  {
    "name": "Kirloskar Oil Engines Limited",
    "ticker": "KIRLOSENG",
    "yf": "KIRLOSENG.NS"
  },
  {
    "name": "Kirloskar Industries Limited",
    "ticker": "KIRLOSIND",
    "yf": "KIRLOSIND.NS"
  },
  {
    "name": "Kirloskar Pneumatic Company Limited",
    "ticker": "KIRLPNU",
    "yf": "KIRLPNU.NS"
  },
  {
    "name": "Kitex Garments Limited",
    "ticker": "KITEX",
    "yf": "KITEX.NS"
  },
  {
    "name": "Kewal Kiran Clothing Limited",
    "ticker": "KKCL",
    "yf": "KKCL.NS"
  },
  {
    "name": "Kilburn Engineering Limited",
    "ticker": "KLBRENG-B",
    "yf": "KLBRENG-B.NS"
  },
  {
    "name": "Knowledge Marine & Engineering Works Limited",
    "ticker": "KMEW",
    "yf": "KMEW.NS"
  },
  {
    "name": "K.M.Sugar Mills Limited",
    "ticker": "KMSUGAR",
    "yf": "KMSUGAR.NS"
  },
  {
    "name": "KN Agri Resources Limited",
    "ticker": "KNAGRI",
    "yf": "KNAGRI.NS"
  },
  {
    "name": "KNR Constructions Limited",
    "ticker": "KNRCON",
    "yf": "KNRCON.NS"
  },
  {
    "name": "Kohinoor Foods Limited",
    "ticker": "KOHINOOR",
    "yf": "KOHINOOR.NS"
  },
  {
    "name": "Kokuyo Camlin Limited",
    "ticker": "KOKUYOCMLN",
    "yf": "KOKUYOCMLN.NS"
  },
  {
    "name": "Kolte - Patil Developers Limited",
    "ticker": "KOLTEPATIL",
    "yf": "KOLTEPATIL.NS"
  },
  {
    "name": "Kopran Limited",
    "ticker": "KOPRAN",
    "yf": "KOPRAN.NS"
  },
  {
    "name": "Kotak Mahindra Bank Limited",
    "ticker": "KOTAKBANK",
    "yf": "KOTAKBANK.NS"
  },
  {
    "name": "Kothari Sugars And Chemicals Limited",
    "ticker": "KOTARISUG",
    "yf": "KOTARISUG.NS"
  },
  {
    "name": "Kothari Petrochemicals Limited",
    "ticker": "KOTHARIPET",
    "yf": "KOTHARIPET.NS"
  },
  {
    "name": "Kothari Products Limited",
    "ticker": "KOTHARIPRO",
    "yf": "KOTHARIPRO.NS"
  },
  {
    "name": "Kothari Industrial Corporation Limited",
    "ticker": "KOTIC",
    "yf": "KOTIC.NS"
  },
  {
    "name": "Kotyark Industries Limited",
    "ticker": "KOTYARK",
    "yf": "KOTYARK.NS"
  },
  {
    "name": "Kovai Medical Center & Hospital Limited",
    "ticker": "KOVAI",
    "yf": "KOVAI.NS"
  },
  {
    "name": "K.P. Energy Limited",
    "ticker": "KPEL",
    "yf": "KPEL.NS"
  },
  {
    "name": "KPI Green Energy Limited",
    "ticker": "KPIGREEN",
    "yf": "KPIGREEN.NS"
  },
  {
    "name": "Kalpataru Projects International Limited",
    "ticker": "KPIL",
    "yf": "KPIL.NS"
  },
  {
    "name": "KPIT Technologies Limited",
    "ticker": "KPITTECH",
    "yf": "KPITTECH.NS"
  },
  {
    "name": "Kwality Pharmaceuticals Limited",
    "ticker": "KPL",
    "yf": "KPL.NS"
  },
  {
    "name": "K.P.R. Mill Limited",
    "ticker": "KPRMILL",
    "yf": "KPRMILL.NS"
  },
  {
    "name": "KRBL Limited",
    "ticker": "KRBL",
    "yf": "KRBL.NS"
  },
  {
    "name": "Kridhan Infra Limited",
    "ticker": "KRIDHANINF",
    "yf": "KRIDHANINF.NS"
  },
  {
    "name": "Krishana Phoschem Limited",
    "ticker": "KRISHANA",
    "yf": "KRISHANA.NS"
  },
  {
    "name": "Krishival Foods Limited",
    "ticker": "KRISHIVAL",
    "yf": "KRISHIVAL.NS"
  },
  {
    "name": "Krishna Defence And Allied Industries Limited",
    "ticker": "KRISHNADEF",
    "yf": "KRISHNADEF.NS"
  },
  {
    "name": "Kriti Industries (India) Limited",
    "ticker": "KRITI",
    "yf": "KRITI.NS"
  },
  {
    "name": "Kritika Wires Limited",
    "ticker": "KRITIKA",
    "yf": "KRITIKA.NS"
  },
  {
    "name": "KRN Heat Exchanger and Refrigeration Limited",
    "ticker": "KRN",
    "yf": "KRN.NS"
  },
  {
    "name": "Kronox Lab Sciences Limited",
    "ticker": "KRONOX",
    "yf": "KRONOX.NS"
  },
  {
    "name": "Kross Limited",
    "ticker": "KROSS",
    "yf": "KROSS.NS"
  },
  {
    "name": "Krsnaa Diagnostics Limited",
    "ticker": "KRSNAA",
    "yf": "KRSNAA.NS"
  },
  {
    "name": "Krystal Integrated Services Limited",
    "ticker": "KRYSTAL",
    "yf": "KRYSTAL.NS"
  },
  {
    "name": "Ksb Limited",
    "ticker": "KSB",
    "yf": "KSB.NS"
  },
  {
    "name": "Kaveri Seed Company Limited",
    "ticker": "KSCL",
    "yf": "KSCL.NS"
  },
  {
    "name": "KSH International Limited",
    "ticker": "KSHINTL",
    "yf": "KSHINTL.NS"
  },
  {
    "name": "Kalyani Steels Limited",
    "ticker": "KSL",
    "yf": "KSL.NS"
  },
  {
    "name": "Ksolves India Limited",
    "ticker": "KSOLVES",
    "yf": "KSOLVES.NS"
  },
  {
    "name": "The Karnataka Bank Limited",
    "ticker": "KTKBANK",
    "yf": "KTKBANK.NS"
  },
  {
    "name": "Kuantum Papers Limited",
    "ticker": "KUANTUM",
    "yf": "KUANTUM.NS"
  },
  {
    "name": "Kwality Wall's (India) Limited",
    "ticker": "KWIL",
    "yf": "KWIL.NS"
  },
  {
    "name": "Lagnam Spintex Limited",
    "ticker": "LAGNAM",
    "yf": "LAGNAM.NS"
  },
  {
    "name": "Lahoti Overseas Limited",
    "ticker": "LAHOTIOV",
    "yf": "LAHOTIOV.NS"
  },
  {
    "name": "Lorenzini Apparels Limited",
    "ticker": "LAL",
    "yf": "LAL.NS"
  },
  {
    "name": "Dr. Lal Path Labs Ltd.",
    "ticker": "LALPATHLAB",
    "yf": "LALPATHLAB.NS"
  },
  {
    "name": "Lambodhara Textiles Limited",
    "ticker": "LAMBODHARA",
    "yf": "LAMBODHARA.NS"
  },
  {
    "name": "Landmark Cars Limited",
    "ticker": "LANDMARK",
    "yf": "LANDMARK.NS"
  },
  {
    "name": "Landsmill Green Limited",
    "ticker": "LANDSMILL",
    "yf": "LANDSMILL.NS"
  },
  {
    "name": "La Opala RG Limited",
    "ticker": "LAOPALA",
    "yf": "LAOPALA.NS"
  },
  {
    "name": "Latent View Analytics Limited",
    "ticker": "LATENTVIEW",
    "yf": "LATENTVIEW.NS"
  },
  {
    "name": "Latteys Industries Limited",
    "ticker": "LATTEYS",
    "yf": "LATTEYS.NS"
  },
  {
    "name": "Laurus Labs Limited",
    "ticker": "LAURUSLABS",
    "yf": "LAURUSLABS.NS"
  },
  {
    "name": "Laxmi Dental Limited",
    "ticker": "LAXMIDENTL",
    "yf": "LAXMIDENTL.NS"
  },
  {
    "name": "Laxmi India Finance Limited",
    "ticker": "LAXMIINDIA",
    "yf": "LAXMIINDIA.NS"
  },
  {
    "name": "Le Merite Exports Limited",
    "ticker": "LEMERITE",
    "yf": "LEMERITE.NS"
  },
  {
    "name": "Lemon Tree Hotels Limited",
    "ticker": "LEMONTREE",
    "yf": "LEMONTREE.NS"
  },
  {
    "name": "Lenskart Solutions Limited",
    "ticker": "LENSKART",
    "yf": "LENSKART.NS"
  },
  {
    "name": "Lakshmi Finance & Industrial Corporation Limited",
    "ticker": "LFIC",
    "yf": "LFIC.NS"
  },
  {
    "name": "LG Balakrishnan & Bros Limited",
    "ticker": "LGBBROSLTD",
    "yf": "LGBBROSLTD.NS"
  },
  {
    "name": "LG Electronics India Limited",
    "ticker": "LGEINDIA",
    "yf": "LGEINDIA.NS"
  },
  {
    "name": "Laxmi Goldorna House Limited",
    "ticker": "LGHL",
    "yf": "LGHL.NS"
  },
  {
    "name": "Libas Consumer Products Limited",
    "ticker": "LIBAS",
    "yf": "LIBAS.NS"
  },
  {
    "name": "Liberty Shoes Limited",
    "ticker": "LIBERTSHOE",
    "yf": "LIBERTSHOE.NS"
  },
  {
    "name": "LIC Housing Finance Limited",
    "ticker": "LICHSGFIN",
    "yf": "LICHSGFIN.NS"
  },
  {
    "name": "Life Insurance Corporation Of India",
    "ticker": "LICI",
    "yf": "LICI.NS"
  },
  {
    "name": "Linc Limited",
    "ticker": "LINC",
    "yf": "LINC.NS"
  },
  {
    "name": "Lincoln Pharmaceuticals Limited",
    "ticker": "LINCOLN",
    "yf": "LINCOLN.NS"
  },
  {
    "name": "Linde India Limited",
    "ticker": "LINDEINDIA",
    "yf": "LINDEINDIA.NS"
  },
  {
    "name": "LLOYDS ENGINEERING WORKS LIMITED",
    "ticker": "LLOYDSENGG",
    "yf": "LLOYDSENGG.NS"
  },
  {
    "name": "Lloyds Enterprises Limited",
    "ticker": "LLOYDSENT",
    "yf": "LLOYDSENT.NS"
  },
  {
    "name": "Lloyds Metals And Energy Limited",
    "ticker": "LLOYDSME",
    "yf": "LLOYDSME.NS"
  },
  {
    "name": "LMW Limited",
    "ticker": "LMW",
    "yf": "LMW.NS"
  },
  {
    "name": "Lodha Developers Limited",
    "ticker": "LODHA",
    "yf": "LODHA.NS"
  },
  {
    "name": "Lords Chloro Alkali Limited",
    "ticker": "LORDSCHLO",
    "yf": "LORDSCHLO.NS"
  },
  {
    "name": "Sri Lotus Developers and Realty Limited",
    "ticker": "LOTUSDEV",
    "yf": "LOTUSDEV.NS"
  },
  {
    "name": "Lotus Eye Hospital and Institute Limited",
    "ticker": "LOTUSEYE",
    "yf": "LOTUSEYE.NS"
  },
  {
    "name": "Lovable Lingerie Limited",
    "ticker": "LOVABLE",
    "yf": "LOVABLE.NS"
  },
  {
    "name": "Larsen & Toubro Limited",
    "ticker": "LT",
    "yf": "LT.NS"
  },
  {
    "name": "L&T Finance Limited",
    "ticker": "LTF",
    "yf": "LTF.NS"
  },
  {
    "name": "LT Foods Limited",
    "ticker": "LTFOODS",
    "yf": "LTFOODS.NS"
  },
  {
    "name": "LTM Limited",
    "ticker": "LTM",
    "yf": "LTM.NS"
  },
  {
    "name": "L&T Technology Services Limited",
    "ticker": "LTTS",
    "yf": "LTTS.NS"
  },
  {
    "name": "Lumax Industries Limited",
    "ticker": "LUMAXIND",
    "yf": "LUMAXIND.NS"
  },
  {
    "name": "Lumax Auto Technologies Limited",
    "ticker": "LUMAXTECH",
    "yf": "LUMAXTECH.NS"
  },
  {
    "name": "Lupin Limited",
    "ticker": "LUPIN",
    "yf": "LUPIN.NS"
  },
  {
    "name": "Lux Industries Limited",
    "ticker": "LUXIND",
    "yf": "LUXIND.NS"
  },
  {
    "name": "Laxmi Organic Industries Limited",
    "ticker": "LXCHEM",
    "yf": "LXCHEM.NS"
  },
  {
    "name": "Lypsa Gems & Jewellery Limited",
    "ticker": "LYPSAGEMS",
    "yf": "LYPSAGEMS.NS"
  },
  {
    "name": "Mahindra & Mahindra Limited",
    "ticker": "M&M",
    "yf": "M&M.NS"
  },
  {
    "name": "Mahindra & Mahindra Financial Services Limited",
    "ticker": "M&MFIN",
    "yf": "M&MFIN.NS"
  },
  {
    "name": "Maan Aluminium Limited",
    "ticker": "MAANALU",
    "yf": "MAANALU.NS"
  },
  {
    "name": "Macpower CNC Machines Limited",
    "ticker": "MACPOWER",
    "yf": "MACPOWER.NS"
  },
  {
    "name": "Madhav Marbles and Granites Limited",
    "ticker": "MADHAV",
    "yf": "MADHAV.NS"
  },
  {
    "name": "Madhav Infra Projects Limited",
    "ticker": "MADHAVIPL",
    "yf": "MADHAVIPL.NS"
  },
  {
    "name": "Madras Fertilizers Limited",
    "ticker": "MADRASFERT",
    "yf": "MADRASFERT.NS"
  },
  {
    "name": "Mafatlal Industries Limited",
    "ticker": "MAFATIND",
    "yf": "MAFATIND.NS"
  },
  {
    "name": "Magadh Sugar & Energy Limited",
    "ticker": "MAGADSUGAR",
    "yf": "MAGADSUGAR.NS"
  },
  {
    "name": "Bank of Maharashtra",
    "ticker": "MAHABANK",
    "yf": "MAHABANK.NS"
  },
  {
    "name": "Maha Rashtra Apex Corporation Limited",
    "ticker": "MAHAPEXLTD",
    "yf": "MAHAPEXLTD.NS"
  },
  {
    "name": "Mahindra EPC Irrigation Limited",
    "ticker": "MAHEPC",
    "yf": "MAHEPC.NS"
  },
  {
    "name": "Maheshwari Logistics Limited",
    "ticker": "MAHESHWARI",
    "yf": "MAHESHWARI.NS"
  },
  {
    "name": "Mahindra Lifespace Developers Limited",
    "ticker": "MAHLIFE",
    "yf": "MAHLIFE.NS"
  },
  {
    "name": "Mahindra Logistics Limited",
    "ticker": "MAHLOG",
    "yf": "MAHLOG.NS"
  },
  {
    "name": "Maharashtra Scooters Limited",
    "ticker": "MAHSCOOTER",
    "yf": "MAHSCOOTER.NS"
  },
  {
    "name": "Maharashtra Seamless Limited",
    "ticker": "MAHSEAMLES",
    "yf": "MAHSEAMLES.NS"
  },
  {
    "name": "Maithan Alloys Limited",
    "ticker": "MAITHANALL",
    "yf": "MAITHANALL.NS"
  },
  {
    "name": "Majestic Auto Limited",
    "ticker": "MAJESAUT",
    "yf": "MAJESAUT.NS"
  },
  {
    "name": "Mallcom (India) Limited",
    "ticker": "MALLCOM",
    "yf": "MALLCOM.NS"
  },
  {
    "name": "Malu Paper Mills Limited",
    "ticker": "MALUPAPER",
    "yf": "MALUPAPER.NS"
  },
  {
    "name": "Mamata Machinery Limited",
    "ticker": "MAMATA",
    "yf": "MAMATA.NS"
  },
  {
    "name": "Manaksia Aluminium Company Limited",
    "ticker": "MANAKALUCO",
    "yf": "MANAKALUCO.NS"
  },
  {
    "name": "Manaksia Coated Metals & Industries Limited",
    "ticker": "MANAKCOAT",
    "yf": "MANAKCOAT.NS"
  },
  {
    "name": "Manaksia Limited",
    "ticker": "MANAKSIA",
    "yf": "MANAKSIA.NS"
  },
  {
    "name": "Manali Petrochemicals Limited",
    "ticker": "MANALIPETC",
    "yf": "MANALIPETC.NS"
  },
  {
    "name": "Manappuram Finance Limited",
    "ticker": "MANAPPURAM",
    "yf": "MANAPPURAM.NS"
  },
  {
    "name": "Manba Finance Limited",
    "ticker": "MANBA",
    "yf": "MANBA.NS"
  },
  {
    "name": "Mangal Credit and Fincorp Limited",
    "ticker": "MANCREDIT",
    "yf": "MANCREDIT.NS"
  },
  {
    "name": "Mangalam Cement Limited",
    "ticker": "MANGLMCEM",
    "yf": "MANGLMCEM.NS"
  },
  {
    "name": "Man Industries (India) Limited",
    "ticker": "MANINDS",
    "yf": "MANINDS.NS"
  },
  {
    "name": "Man Infraconstruction Limited",
    "ticker": "MANINFRA",
    "yf": "MANINFRA.NS"
  },
  {
    "name": "Mankind Pharma Limited",
    "ticker": "MANKIND",
    "yf": "MANKIND.NS"
  },
  {
    "name": "Manomay Tex India Limited",
    "ticker": "MANOMAY",
    "yf": "MANOMAY.NS"
  },
  {
    "name": "Manorama Industries Limited",
    "ticker": "MANORAMA",
    "yf": "MANORAMA.NS"
  },
  {
    "name": "Mangalam Organics Limited",
    "ticker": "MANORG",
    "yf": "MANORG.NS"
  },
  {
    "name": "Manugraph India Limited",
    "ticker": "MANUGRAPH",
    "yf": "MANUGRAPH.NS"
  },
  {
    "name": "Vedant Fashions Limited",
    "ticker": "MANYAVAR",
    "yf": "MANYAVAR.NS"
  },
  {
    "name": "C.E. Info Systems Limited",
    "ticker": "MAPMYINDIA",
    "yf": "MAPMYINDIA.NS"
  },
  {
    "name": "Maral Overseas Limited",
    "ticker": "MARALOVER",
    "yf": "MARALOVER.NS"
  },
  {
    "name": "Marathon Nextgen Realty Limited",
    "ticker": "MARATHON",
    "yf": "MARATHON.NS"
  },
  {
    "name": "Marico Limited",
    "ticker": "MARICO",
    "yf": "MARICO.NS"
  },
  {
    "name": "Marine Electricals (India) Limited",
    "ticker": "MARINE",
    "yf": "MARINE.NS"
  },
  {
    "name": "Markolines Pavement Technologies Limited",
    "ticker": "MARKOLINES",
    "yf": "MARKOLINES.NS"
  },
  {
    "name": "Marksans Pharma Limited",
    "ticker": "MARKSANS",
    "yf": "MARKSANS.NS"
  },
  {
    "name": "Marsons Limited",
    "ticker": "MARSONS",
    "yf": "MARSONS.NS"
  },
  {
    "name": "Maruti Suzuki India Limited",
    "ticker": "MARUTI",
    "yf": "MARUTI.NS"
  },
  {
    "name": "MAS Financial Services Limited",
    "ticker": "MASFIN",
    "yf": "MASFIN.NS"
  },
  {
    "name": "Mastek Limited",
    "ticker": "MASTEK",
    "yf": "MASTEK.NS"
  },
  {
    "name": "Master Trust Limited",
    "ticker": "MASTERTR",
    "yf": "MASTERTR.NS"
  },
  {
    "name": "Matrimony.Com Limited",
    "ticker": "MATRIMONY",
    "yf": "MATRIMONY.NS"
  },
  {
    "name": "Mawana Sugars Limited",
    "ticker": "MAWANASUG",
    "yf": "MAWANASUG.NS"
  },
  {
    "name": "Max Estates Limited",
    "ticker": "MAXESTATES",
    "yf": "MAXESTATES.NS"
  },
  {
    "name": "Max Healthcare Institute Limited",
    "ticker": "MAXHEALTH",
    "yf": "MAXHEALTH.NS"
  },
  {
    "name": "Max India Limited",
    "ticker": "MAXIND",
    "yf": "MAXIND.NS"
  },
  {
    "name": "Mayur Uniquoters Ltd",
    "ticker": "MAYURUNIQ",
    "yf": "MAYURUNIQ.NS"
  },
  {
    "name": "Mazda Limited",
    "ticker": "MAZDA",
    "yf": "MAZDA.NS"
  },
  {
    "name": "Mazagon Dock Shipbuilders Limited",
    "ticker": "MAZDOCK",
    "yf": "MAZDOCK.NS"
  },
  {
    "name": "Madhya Bharat Agro Products Limited",
    "ticker": "MBAPL",
    "yf": "MBAPL.NS"
  },
  {
    "name": "M & B Engineering Limited",
    "ticker": "MBEL",
    "yf": "MBEL.NS"
  },
  {
    "name": "Mac Charles India Limited",
    "ticker": "MCCHRLS-B",
    "yf": "MCCHRLS-B.NS"
  },
  {
    "name": "Magellanic Cloud Limited",
    "ticker": "MCLOUD",
    "yf": "MCLOUD.NS"
  },
  {
    "name": "Multi Commodity Exchange of India Limited",
    "ticker": "MCX",
    "yf": "MCX.NS"
  },
  {
    "name": "Global Health Limited",
    "ticker": "MEDANTA",
    "yf": "MEDANTA.NS"
  },
  {
    "name": "Medi Assist Healthcare Services Limited",
    "ticker": "MEDIASSIST",
    "yf": "MEDIASSIST.NS"
  },
  {
    "name": "Medicamen Biotech Limited",
    "ticker": "MEDICAMEQ",
    "yf": "MEDICAMEQ.NS"
  },
  {
    "name": "Medico Remedies Limited",
    "ticker": "MEDICO",
    "yf": "MEDICO.NS"
  },
  {
    "name": "Medplus Health Services Limited",
    "ticker": "MEDPLUS",
    "yf": "MEDPLUS.NS"
  },
  {
    "name": "Meesho Limited",
    "ticker": "MEESHO",
    "yf": "MEESHO.NS"
  },
  {
    "name": "Megastar Foods Limited",
    "ticker": "MEGASTAR",
    "yf": "MEGASTAR.NS"
  },
  {
    "name": "Menon Pistons Limited",
    "ticker": "MENNPIS",
    "yf": "MENNPIS.NS"
  },
  {
    "name": "Menon Bearings Limited",
    "ticker": "MENONBE",
    "yf": "MENONBE.NS"
  },
  {
    "name": "Mercantile Ventures Limited",
    "ticker": "MERCANTILE",
    "yf": "MERCANTILE.NS"
  },
  {
    "name": "Metro Brands Limited",
    "ticker": "METROBRAND",
    "yf": "METROBRAND.NS"
  },
  {
    "name": "Metroglobal Limited",
    "ticker": "METROGLOBL",
    "yf": "METROGLOBL.NS"
  },
  {
    "name": "Metropolis Healthcare Limited",
    "ticker": "METROPOLIS",
    "yf": "METROPOLIS.NS"
  },
  {
    "name": "Mahalaxmi Fabric Mills Limited",
    "ticker": "MFML",
    "yf": "MFML.NS"
  },
  {
    "name": "Max Financial Services Limited",
    "ticker": "MFSL",
    "yf": "MFSL.NS"
  },
  {
    "name": "Mangalam Global Enterprise Limited",
    "ticker": "MGEL",
    "yf": "MGEL.NS"
  },
  {
    "name": "Mahanagar Gas Limited",
    "ticker": "MGL",
    "yf": "MGL.NS"
  },
  {
    "name": "Mahalaxmi Rubtech Limited",
    "ticker": "MHLXMIRU",
    "yf": "MHLXMIRU.NS"
  },
  {
    "name": "Mahindra Holidays & Resorts India Limited",
    "ticker": "MHRIL",
    "yf": "MHRIL.NS"
  },
  {
    "name": "MIC Electronics Limited",
    "ticker": "MICEL",
    "yf": "MICEL.NS"
  },
  {
    "name": "Mishra Dhatu Nigam Limited",
    "ticker": "MIDHANI",
    "yf": "MIDHANI.NS"
  },
  {
    "name": "Midwest Limited",
    "ticker": "MIDWESTLTD",
    "yf": "MIDWESTLTD.NS"
  },
  {
    "name": "Minda Corporation Limited",
    "ticker": "MINDACORP",
    "yf": "MINDACORP.NS"
  },
  {
    "name": "Mindteck (India) Limited",
    "ticker": "MINDTECK",
    "yf": "MINDTECK.NS"
  },
  {
    "name": "MIRC Electronics Limited",
    "ticker": "MIRCELECTR",
    "yf": "MIRCELECTR.NS"
  },
  {
    "name": "Mirza International Limited",
    "ticker": "MIRZAINT",
    "yf": "MIRZAINT.NS"
  },
  {
    "name": "MITCON Consultancy & Engineering Services Limited",
    "ticker": "MITCON",
    "yf": "MITCON.NS"
  },
  {
    "name": "Mittal Life Style Limited",
    "ticker": "MITTAL",
    "yf": "MITTAL.NS"
  },
  {
    "name": "M K Proteins Limited",
    "ticker": "MKPL",
    "yf": "MKPL.NS"
  },
  {
    "name": "MM Forgings Limited",
    "ticker": "MMFL",
    "yf": "MMFL.NS"
  },
  {
    "name": "MMP Industries Limited",
    "ticker": "MMP",
    "yf": "MMP.NS"
  },
  {
    "name": "MMTC Limited",
    "ticker": "MMTC",
    "yf": "MMTC.NS"
  },
  {
    "name": "Media Matrix Worldwide Limited",
    "ticker": "MMWL",
    "yf": "MMWL.NS"
  },
  {
    "name": "One Mobikwik Systems Limited",
    "ticker": "MOBIKWIK",
    "yf": "MOBIKWIK.NS"
  },
  {
    "name": "Modi Naturals Limited",
    "ticker": "MODINATUR",
    "yf": "MODINATUR.NS"
  },
  {
    "name": "Modi Rubber Limited",
    "ticker": "MODIRUBBER",
    "yf": "MODIRUBBER.NS"
  },
  {
    "name": "Modis Navnirman Limited",
    "ticker": "MODIS",
    "yf": "MODIS.NS"
  },
  {
    "name": "MODISON LIMITED",
    "ticker": "MODISONLTD",
    "yf": "MODISONLTD.NS"
  },
  {
    "name": "Modern Threads (India) Limited",
    "ticker": "MODTHREAD",
    "yf": "MODTHREAD.NS"
  },
  {
    "name": "Mohit Industries Limited",
    "ticker": "MOHITIND",
    "yf": "MOHITIND.NS"
  },
  {
    "name": "MOIL Limited",
    "ticker": "MOIL",
    "yf": "MOIL.NS"
  },
  {
    "name": "Moksh Ornaments Limited",
    "ticker": "MOKSH",
    "yf": "MOKSH.NS"
  },
  {
    "name": "Meghmani Organics Limited",
    "ticker": "MOL",
    "yf": "MOL.NS"
  },
  {
    "name": "Mold-Tek Technologies Limited",
    "ticker": "MOLDTECH",
    "yf": "MOLDTECH.NS"
  },
  {
    "name": "Mold-Tek Packaging Limited",
    "ticker": "MOLDTKPAC",
    "yf": "MOLDTKPAC.NS"
  },
  {
    "name": "Monarch Networth Capital Limited",
    "ticker": "MONARCH",
    "yf": "MONARCH.NS"
  },
  {
    "name": "Moneyboxx Finance Limited",
    "ticker": "MONEYBOXX",
    "yf": "MONEYBOXX.NS"
  },
  {
    "name": "Monte Carlo Fashions Limited",
    "ticker": "MONTECARLO",
    "yf": "MONTECARLO.NS"
  },
  {
    "name": "Morepen Laboratories Limited",
    "ticker": "MOREPENLAB",
    "yf": "MOREPENLAB.NS"
  },
  {
    "name": "Moschip Technologies Limited",
    "ticker": "MOSCHIP",
    "yf": "MOSCHIP.NS"
  },
  {
    "name": "Samvardhana Motherson International Limited",
    "ticker": "MOTHERSON",
    "yf": "MOTHERSON.NS"
  },
  {
    "name": "Motilal Oswal Financial Services Limited",
    "ticker": "MOTILALOFS",
    "yf": "MOTILALOFS.NS"
  },
  {
    "name": "Motisons Jewellers Limited",
    "ticker": "MOTISONS",
    "yf": "MOTISONS.NS"
  },
  {
    "name": "The Motor & General Finance Limited",
    "ticker": "MOTOGENFIN",
    "yf": "MOTOGENFIN.NS"
  },
  {
    "name": "MphasiS Limited",
    "ticker": "MPHASIS",
    "yf": "MPHASIS.NS"
  },
  {
    "name": "MPS Limited",
    "ticker": "MPSLTD",
    "yf": "MPSLTD.NS"
  },
  {
    "name": "MRF Limited",
    "ticker": "MRF",
    "yf": "MRF.NS"
  },
  {
    "name": "Mangalore Refinery and Petrochemicals Limited",
    "ticker": "MRPL",
    "yf": "MRPL.NS"
  },
  {
    "name": "MSP Steel & Power Limited",
    "ticker": "MSPL",
    "yf": "MSPL.NS"
  },
  {
    "name": "Mstc Limited",
    "ticker": "MSTCLTD",
    "yf": "MSTCLTD.NS"
  },
  {
    "name": "Motherson Sumi Wiring India Limited",
    "ticker": "MSUMI",
    "yf": "MSUMI.NS"
  },
  {
    "name": "Mtar Technologies Limited",
    "ticker": "MTARTECH",
    "yf": "MTARTECH.NS"
  },
  {
    "name": "Mahanagar Telephone Nigam Limited",
    "ticker": "MTNL",
    "yf": "MTNL.NS"
  },
  {
    "name": "Mufin Green Finance Limited",
    "ticker": "MUFIN",
    "yf": "MUFIN.NS"
  },
  {
    "name": "Credo Brands Marketing Limited",
    "ticker": "MUFTI",
    "yf": "MUFTI.NS"
  },
  {
    "name": "Mukand Limited",
    "ticker": "MUKANDLTD",
    "yf": "MUKANDLTD.NS"
  },
  {
    "name": "Mukka Proteins Limited",
    "ticker": "MUKKA",
    "yf": "MUKKA.NS"
  },
  {
    "name": "Mukta Arts Limited",
    "ticker": "MUKTAARTS",
    "yf": "MUKTAARTS.NS"
  },
  {
    "name": "Munjal Auto Industries Limited",
    "ticker": "MUNJALAU",
    "yf": "MUNJALAU.NS"
  },
  {
    "name": "Munjal Showa Limited",
    "ticker": "MUNJALSHOW",
    "yf": "MUNJALSHOW.NS"
  },
  {
    "name": "Murudeshwar Ceramics Limited",
    "ticker": "MURUDCERA",
    "yf": "MURUDCERA.NS"
  },
  {
    "name": "Muthoot Capital Services Limited",
    "ticker": "MUTHOOTCAP",
    "yf": "MUTHOOTCAP.NS"
  },
  {
    "name": "Muthoot Finance Limited",
    "ticker": "MUTHOOTFIN",
    "yf": "MUTHOOTFIN.NS"
  },
  {
    "name": "Muthoot Microfin Limited",
    "ticker": "MUTHOOTMF",
    "yf": "MUTHOOTMF.NS"
  },
  {
    "name": "Manoj Vaibhav Gems N Jewellers Limited",
    "ticker": "MVGJL",
    "yf": "MVGJL.NS"
  },
  {
    "name": "Mangalam Worldwide Limited",
    "ticker": "MWL",
    "yf": "MWL.NS"
  },
  {
    "name": "NACL Industries Limited",
    "ticker": "NACLIND",
    "yf": "NACLIND.NS"
  },
  {
    "name": "Nagreeka Exports Limited",
    "ticker": "NAGREEKEXP",
    "yf": "NAGREEKEXP.NS"
  },
  {
    "name": "Nahar Capital and Financial Services Limited",
    "ticker": "NAHARCAP",
    "yf": "NAHARCAP.NS"
  },
  {
    "name": "Nahar Industrial Enterprises Limited",
    "ticker": "NAHARINDUS",
    "yf": "NAHARINDUS.NS"
  },
  {
    "name": "Nahar Poly Films Limited",
    "ticker": "NAHARPOLY",
    "yf": "NAHARPOLY.NS"
  },
  {
    "name": "Nippon Life India Asset Management Limited",
    "ticker": "NAM-INDIA",
    "yf": "NAM-INDIA.NS"
  },
  {
    "name": "Narmada Agrobase Limited",
    "ticker": "NARMADA",
    "yf": "NARMADA.NS"
  },
  {
    "name": "Natural Capsules Limited",
    "ticker": "NATCAPSUQ",
    "yf": "NATCAPSUQ.NS"
  },
  {
    "name": "Natco Pharma Limited",
    "ticker": "NATCOPHARM",
    "yf": "NATCOPHARM.NS"
  },
  {
    "name": "Nath Bio-Genes (India) Limited",
    "ticker": "NATHBIOGEN",
    "yf": "NATHBIOGEN.NS"
  },
  {
    "name": "National Aluminium Company Limited",
    "ticker": "NATIONALUM",
    "yf": "NATIONALUM.NS"
  },
  {
    "name": "National Standard (India) Limited",
    "ticker": "NATIONSTD",
    "yf": "NATIONSTD.NS"
  },
  {
    "name": "Info Edge (India) Limited",
    "ticker": "NAUKRI",
    "yf": "NAUKRI.NS"
  },
  {
    "name": "NAVA LIMITED",
    "ticker": "NAVA",
    "yf": "NAVA.NS"
  },
  {
    "name": "Navin Fluorine International Limited",
    "ticker": "NAVINFLUOR",
    "yf": "NAVINFLUOR.NS"
  },
  {
    "name": "Navkar Corporation Limited",
    "ticker": "NAVKARCORP",
    "yf": "NAVKARCORP.NS"
  },
  {
    "name": "Navkar Urbanstructure Limited",
    "ticker": "NAVKARURB",
    "yf": "NAVKARURB.NS"
  },
  {
    "name": "Navneet Education Limited",
    "ticker": "NAVNETEDUL",
    "yf": "NAVNETEDUL.NS"
  },
  {
    "name": "Nazara Technologies Limited",
    "ticker": "NAZARA",
    "yf": "NAZARA.NS"
  },
  {
    "name": "NBCC (India) Limited",
    "ticker": "NBCC",
    "yf": "NBCC.NS"
  },
  {
    "name": "N. B. I. Industrial Finance Company Limited",
    "ticker": "NBIFIN",
    "yf": "NBIFIN.NS"
  },
  {
    "name": "NCC Limited",
    "ticker": "NCC",
    "yf": "NCC.NS"
  },
  {
    "name": "NCL Industries Limited",
    "ticker": "NCLIND",
    "yf": "NCLIND.NS"
  },
  {
    "name": "Naga Dhunseri Group Limited",
    "ticker": "NDGL",
    "yf": "NDGL.NS"
  },
  {
    "name": "Nandan Denim Limited",
    "ticker": "NDL",
    "yf": "NDL.NS"
  },
  {
    "name": "NDL Ventures Limited",
    "ticker": "NDLVENTURE",
    "yf": "NDLVENTURE.NS"
  },
  {
    "name": "Ndr Auto Components Limited",
    "ticker": "NDRAUTO",
    "yf": "NDRAUTO.NS"
  },
  {
    "name": "New Delhi Television Limited",
    "ticker": "NDTV",
    "yf": "NDTV.NS"
  },
  {
    "name": "Neelamalai Agro Industries Limited",
    "ticker": "NEAGI",
    "yf": "NEAGI.NS"
  },
  {
    "name": "North Eastern Carrying Corporation Limited",
    "ticker": "NECCLTD",
    "yf": "NECCLTD.NS"
  },
  {
    "name": "Nectar Lifesciences Limited",
    "ticker": "NECLIFE",
    "yf": "NECLIFE.NS"
  },
  {
    "name": "Nelcast Limited",
    "ticker": "NELCAST",
    "yf": "NELCAST.NS"
  },
  {
    "name": "NELCO Limited",
    "ticker": "NELCO",
    "yf": "NELCO.NS"
  },
  {
    "name": "Neogen Chemicals Limited",
    "ticker": "NEOGEN",
    "yf": "NEOGEN.NS"
  },
  {
    "name": "Nephrocare Health Services Limited",
    "ticker": "NEPHROPLUS",
    "yf": "NEPHROPLUS.NS"
  },
  {
    "name": "Nesco Limited",
    "ticker": "NESCO",
    "yf": "NESCO.NS"
  },
  {
    "name": "Nestle India Limited",
    "ticker": "NESTLEIND",
    "yf": "NESTLEIND.NS"
  },
  {
    "name": "Netweb Technologies India Limited",
    "ticker": "NETWEB",
    "yf": "NETWEB.NS"
  },
  {
    "name": "Network18 Media & Investments Limited",
    "ticker": "NETWORK18",
    "yf": "NETWORK18.NS"
  },
  {
    "name": "Neuland Laboratories Limited",
    "ticker": "NEULANDLAB",
    "yf": "NEULANDLAB.NS"
  },
  {
    "name": "Newgen Software Technologies Limited",
    "ticker": "NEWGEN",
    "yf": "NEWGEN.NS"
  },
  {
    "name": "Next Mediaworks Limited",
    "ticker": "NEXTMEDIA",
    "yf": "NEXTMEDIA.NS"
  },
  {
    "name": "National Fertilizers Limited",
    "ticker": "NFL",
    "yf": "NFL.NS"
  },
  {
    "name": "Nakoda Group of Industries Limited",
    "ticker": "NGIL",
    "yf": "NGIL.NS"
  },
  {
    "name": "NGL Fine-Chem Limited",
    "ticker": "NGLFINE",
    "yf": "NGLFINE.NS"
  },
  {
    "name": "Narayana Hrudayalaya Ltd.",
    "ticker": "NH",
    "yf": "NH.NS"
  },
  {
    "name": "NHPC Limited",
    "ticker": "NHPC",
    "yf": "NHPC.NS"
  },
  {
    "name": "The New India Assurance Company Limited",
    "ticker": "NIACL",
    "yf": "NIACL.NS"
  },
  {
    "name": "NIBE Limited",
    "ticker": "NIBE",
    "yf": "NIBE.NS"
  },
  {
    "name": "NRB Industrial Bearings Limited",
    "ticker": "NIBL",
    "yf": "NIBL.NS"
  },
  {
    "name": "NIIT Limited",
    "ticker": "NIITLTD",
    "yf": "NIITLTD.NS"
  },
  {
    "name": "NIIT Learning Systems Limited",
    "ticker": "NIITMTS",
    "yf": "NIITMTS.NS"
  },
  {
    "name": "Nila Infrastructures Limited",
    "ticker": "NILAINFRA",
    "yf": "NILAINFRA.NS"
  },
  {
    "name": "Nila Spaces Limited",
    "ticker": "NILASPACES",
    "yf": "NILASPACES.NS"
  },
  {
    "name": "Nile Limited",
    "ticker": "NILE",
    "yf": "NILE.NS"
  },
  {
    "name": "Nilkamal Limited",
    "ticker": "NILKAMAL",
    "yf": "NILKAMAL.NS"
  },
  {
    "name": "Nimbus Projects Limited",
    "ticker": "NIMBSPROJ",
    "yf": "NIMBSPROJ.NS"
  },
  {
    "name": "Indo-National Limited",
    "ticker": "NIPPOBATRY",
    "yf": "NIPPOBATRY.NS"
  },
  {
    "name": "Niraj Cement Structurals Limited",
    "ticker": "NIRAJ",
    "yf": "NIRAJ.NS"
  },
  {
    "name": "Nirlon Limited",
    "ticker": "NIRLON",
    "yf": "NIRLON.NS"
  },
  {
    "name": "Nitco Limited",
    "ticker": "NITCO",
    "yf": "NITCO.NS"
  },
  {
    "name": "Nitin Spinners Limited",
    "ticker": "NITINSPIN",
    "yf": "NITINSPIN.NS"
  },
  {
    "name": "Nitiraj Engineers Limited",
    "ticker": "NITIRAJ",
    "yf": "NITIRAJ.NS"
  },
  {
    "name": "Nitta Gelatin India Limited",
    "ticker": "NITTAGELA",
    "yf": "NITTAGELA.NS"
  },
  {
    "name": "Niva Bupa Health Insurance Company Limited",
    "ticker": "NIVABUPA",
    "yf": "NIVABUPA.NS"
  },
  {
    "name": "NK Industries Limited",
    "ticker": "NKIND",
    "yf": "NKIND.NS"
  },
  {
    "name": "NLC India Limited",
    "ticker": "NLCINDIA",
    "yf": "NLCINDIA.NS"
  },
  {
    "name": "NMDC Limited",
    "ticker": "NMDC",
    "yf": "NMDC.NS"
  },
  {
    "name": "NOCIL Limited",
    "ticker": "NOCIL",
    "yf": "NOCIL.NS"
  },
  {
    "name": "Noida Toll Bridge Company Limited",
    "ticker": "NOIDATOLL",
    "yf": "NOIDATOLL.NS"
  },
  {
    "name": "Norben Tea & Exports Limited",
    "ticker": "NORBTEAEXP",
    "yf": "NORBTEAEXP.NS"
  },
  {
    "name": "Northern Arc Capital Limited",
    "ticker": "NORTHARC",
    "yf": "NORTHARC.NS"
  },
  {
    "name": "Nova Agritech Limited",
    "ticker": "NOVAAGRI",
    "yf": "NOVAAGRI.NS"
  },
  {
    "name": "Novartis India Limited",
    "ticker": "NOVARTIND",
    "yf": "NOVARTIND.NS"
  },
  {
    "name": "Network People Services Technologies Limited",
    "ticker": "NPST",
    "yf": "NPST.NS"
  },
  {
    "name": "N R Agarwal Industries Limited",
    "ticker": "NRAIL",
    "yf": "NRAIL.NS"
  },
  {
    "name": "NRB Bearing Limited",
    "ticker": "NRBBEARING",
    "yf": "NRBBEARING.NS"
  },
  {
    "name": "Nupur Recyclers Limited",
    "ticker": "NRL",
    "yf": "NRL.NS"
  },
  {
    "name": "Nalwa Sons Investments Limited",
    "ticker": "NSIL",
    "yf": "NSIL.NS"
  },
  {
    "name": "NMDC Steel Limited",
    "ticker": "NSLNISP",
    "yf": "NSLNISP.NS"
  },
  {
    "name": "NTPC Limited",
    "ticker": "NTPC",
    "yf": "NTPC.NS"
  },
  {
    "name": "NTPC Green Energy Limited",
    "ticker": "NTPCGREEN",
    "yf": "NTPCGREEN.NS"
  },
  {
    "name": "Nucleus Software Exports Limited",
    "ticker": "NUCLEUS",
    "yf": "NUCLEUS.NS"
  },
  {
    "name": "Nureca Limited",
    "ticker": "NURECA",
    "yf": "NURECA.NS"
  },
  {
    "name": "Nuvama Wealth Management Limited",
    "ticker": "NUVAMA",
    "yf": "NUVAMA.NS"
  },
  {
    "name": "Nuvoco Vistas Corporation Limited",
    "ticker": "NUVOCO",
    "yf": "NUVOCO.NS"
  },
  {
    "name": "FSN E-Commerce Ventures Limited",
    "ticker": "NYKAA",
    "yf": "NYKAA.NS"
  },
  {
    "name": "Oriental Aromatics Limited",
    "ticker": "OAL",
    "yf": "OAL.NS"
  },
  {
    "name": "Orissa Bengal Carrier Limited",
    "ticker": "OBCL",
    "yf": "OBCL.NS"
  },
  {
    "name": "Oberoi Realty Limited",
    "ticker": "OBEROIRLTY",
    "yf": "OBEROIRLTY.NS"
  },
  {
    "name": "OCCL Limited",
    "ticker": "OCCLLTD",
    "yf": "OCCLLTD.NS"
  },
  {
    "name": "Oracle Financial Services Software Limited",
    "ticker": "OFSS",
    "yf": "OFSS.NS"
  },
  {
    "name": "Oil India Limited",
    "ticker": "OIL",
    "yf": "OIL.NS"
  },
  {
    "name": "Ola Electric Mobility Limited",
    "ticker": "OLAELEC",
    "yf": "OLAELEC.NS"
  },
  {
    "name": "Olectra Greentech Limited",
    "ticker": "OLECTRA",
    "yf": "OLECTRA.NS"
  },
  {
    "name": "Omax Autos Limited",
    "ticker": "OMAXAUTO",
    "yf": "OMAXAUTO.NS"
  },
  {
    "name": "Omaxe Limited",
    "ticker": "OMAXE",
    "yf": "OMAXE.NS"
  },
  {
    "name": "Om Freight Forwarders Limited",
    "ticker": "OMFREIGHT",
    "yf": "OMFREIGHT.NS"
  },
  {
    "name": "OM INFRA LIMITED",
    "ticker": "OMINFRAL",
    "yf": "OMINFRAL.NS"
  },
  {
    "name": "Omnitech Engineering Limited",
    "ticker": "OMNI",
    "yf": "OMNI.NS"
  },
  {
    "name": "Onelife Capital Advisors Limited",
    "ticker": "ONELIFECAP",
    "yf": "ONELIFECAP.NS"
  },
  {
    "name": "One Point One Solutions Limited",
    "ticker": "ONEPOINT",
    "yf": "ONEPOINT.NS"
  },
  {
    "name": "Onesource Specialty Pharma Limited",
    "ticker": "ONESOURCE",
    "yf": "ONESOURCE.NS"
  },
  {
    "name": "Oil & Natural Gas Corporation Limited",
    "ticker": "ONGC",
    "yf": "ONGC.NS"
  },
  {
    "name": "OnMobile Global Limited",
    "ticker": "ONMOBILE",
    "yf": "ONMOBILE.NS"
  },
  {
    "name": "Onward Technologies Limited",
    "ticker": "ONWARDTEC",
    "yf": "ONWARDTEC.NS"
  },
  {
    "name": "Optiemus Infracom Limited",
    "ticker": "OPTIEMUS",
    "yf": "OPTIEMUS.NS"
  },
  {
    "name": "Orbit Exports Limited",
    "ticker": "ORBTEXP",
    "yf": "ORBTEXP.NS"
  },
  {
    "name": "Orchasp Limited",
    "ticker": "ORCHASP",
    "yf": "ORCHASP.NS"
  },
  {
    "name": "Orchid Pharma Limited",
    "ticker": "ORCHPHARMA",
    "yf": "ORCHPHARMA.NS"
  },
  {
    "name": "Oricon Enterprises Limited",
    "ticker": "ORICONENT",
    "yf": "ORICONENT.NS"
  },
  {
    "name": "Oriental Trimex Limited",
    "ticker": "ORIENTALTL",
    "yf": "ORIENTALTL.NS"
  },
  {
    "name": "Orient Bell Limited",
    "ticker": "ORIENTBELL",
    "yf": "ORIENTBELL.NS"
  },
  {
    "name": "Orient Cement Limited",
    "ticker": "ORIENTCEM",
    "yf": "ORIENTCEM.NS"
  },
  {
    "name": "ORIENT CERATECH LIMITED",
    "ticker": "ORIENTCER",
    "yf": "ORIENTCER.NS"
  },
  {
    "name": "Orient Electric Limited",
    "ticker": "ORIENTELEC",
    "yf": "ORIENTELEC.NS"
  },
  {
    "name": "Oriental Hotels Limited",
    "ticker": "ORIENTHOT",
    "yf": "ORIENTHOT.NS"
  },
  {
    "name": "Orient Press Limited",
    "ticker": "ORIENTLTD",
    "yf": "ORIENTLTD.NS"
  },
  {
    "name": "Orient Paper & Industries Limited",
    "ticker": "ORIENTPPR",
    "yf": "ORIENTPPR.NS"
  },
  {
    "name": "Orient Technologies Limited",
    "ticker": "ORIENTTECH",
    "yf": "ORIENTTECH.NS"
  },
  {
    "name": "The Orissa Minerals Development Company Limited",
    "ticker": "ORISSAMINE",
    "yf": "ORISSAMINE.NS"
  },
  {
    "name": "Orkla India Limited",
    "ticker": "ORKLAINDIA",
    "yf": "ORKLAINDIA.NS"
  },
  {
    "name": "Osia Hyper Retail Limited",
    "ticker": "OSIAHYPER",
    "yf": "OSIAHYPER.NS"
  },
  {
    "name": "Oswal Greentech Limited",
    "ticker": "OSWALGREEN",
    "yf": "OSWALGREEN.NS"
  },
  {
    "name": "Oswal Pumps Limited",
    "ticker": "OSWALPUMPS",
    "yf": "OSWALPUMPS.NS"
  },
  {
    "name": "ShreeOswal Seeds And Chemicals Limited",
    "ticker": "OSWALSEEDS",
    "yf": "OSWALSEEDS.NS"
  },
  {
    "name": "Pace Digitek Limited",
    "ticker": "PACEDIGITK",
    "yf": "PACEDIGITK.NS"
  },
  {
    "name": "Page Industries Limited",
    "ticker": "PAGEIND",
    "yf": "PAGEIND.NS"
  },
  {
    "name": "Paisalo Digital Limited",
    "ticker": "PAISALO",
    "yf": "PAISALO.NS"
  },
  {
    "name": "PAKKA LIMITED",
    "ticker": "PAKKA",
    "yf": "PAKKA.NS"
  },
  {
    "name": "Palash Securities Limited",
    "ticker": "PALASHSECU",
    "yf": "PALASHSECU.NS"
  },
  {
    "name": "Panacea Biotec Limited",
    "ticker": "PANACEABIO",
    "yf": "PANACEABIO.NS"
  },
  {
    "name": "Panama Petrochem Limited",
    "ticker": "PANAMAPET",
    "yf": "PANAMAPET.NS"
  },
  {
    "name": "Pansari Developers Limited",
    "ticker": "PANSARI",
    "yf": "PANSARI.NS"
  },
  {
    "name": "Par Drugs And Chemicals Limited",
    "ticker": "PAR",
    "yf": "PAR.NS"
  },
  {
    "name": "Paramount Communications Limited",
    "ticker": "PARACABLES",
    "yf": "PARACABLES.NS"
  },
  {
    "name": "Paradeep Phosphates Limited",
    "ticker": "PARADEEP",
    "yf": "PARADEEP.NS"
  },
  {
    "name": "Parag Milk Foods Limited",
    "ticker": "PARAGMILK",
    "yf": "PARAGMILK.NS"
  },
  {
    "name": "Paras Defence and Space Technologies Limited",
    "ticker": "PARAS",
    "yf": "PARAS.NS"
  },
  {
    "name": "Park Medi World Limited",
    "ticker": "PARKHOSPS",
    "yf": "PARKHOSPS.NS"
  },
  {
    "name": "Apeejay Surrendra Park Hotels Limited",
    "ticker": "PARKHOTELS",
    "yf": "PARKHOTELS.NS"
  },
  {
    "name": "Pashupati Cotspin Limited",
    "ticker": "PASHUPATI",
    "yf": "PASHUPATI.NS"
  },
  {
    "name": "Pasupati Acrylon Limited",
    "ticker": "PASUPTAC",
    "yf": "PASUPTAC.NS"
  },
  {
    "name": "Patanjali Foods Limited",
    "ticker": "PATANJALI",
    "yf": "PATANJALI.NS"
  },
  {
    "name": "Patel Engineering Limited",
    "ticker": "PATELENG",
    "yf": "PATELENG.NS"
  },
  {
    "name": "Patel Retail Limited",
    "ticker": "PATELRMART",
    "yf": "PATELRMART.NS"
  },
  {
    "name": "Patel Integrated Logistics Limited",
    "ticker": "PATINTLOG",
    "yf": "PATINTLOG.NS"
  },
  {
    "name": "Paushak Limited",
    "ticker": "PAUSHAKLTD",
    "yf": "PAUSHAKLTD.NS"
  },
  {
    "name": "One 97 Communications Limited",
    "ticker": "PAYTM",
    "yf": "PAYTM.NS"
  },
  {
    "name": "PCBL Chemical Limited",
    "ticker": "PCBL",
    "yf": "PCBL.NS"
  },
  {
    "name": "PC Jeweller Limited",
    "ticker": "PCJEWELLER",
    "yf": "PCJEWELLER.NS"
  },
  {
    "name": "Pudumjee Paper Products Limited",
    "ticker": "PDMJEPAPER",
    "yf": "PDMJEPAPER.NS"
  },
  {
    "name": "PDS Limited",
    "ticker": "PDSL",
    "yf": "PDSL.NS"
  },
  {
    "name": "Pennar Industries Limited",
    "ticker": "PENIND",
    "yf": "PENIND.NS"
  },
  {
    "name": "Persistent Systems Limited",
    "ticker": "PERSISTENT",
    "yf": "PERSISTENT.NS"
  },
  {
    "name": "Petronet LNG Limited",
    "ticker": "PETRONET",
    "yf": "PETRONET.NS"
  },
  {
    "name": "Power Finance Corporation Limited",
    "ticker": "PFC",
    "yf": "PFC.NS"
  },
  {
    "name": "Pfizer Limited",
    "ticker": "PFIZER",
    "yf": "PFIZER.NS"
  },
  {
    "name": "Prime Focus Limited",
    "ticker": "PFOCUS",
    "yf": "PFOCUS.NS"
  },
  {
    "name": "PTC India Financial Services Limited",
    "ticker": "PFS",
    "yf": "PFS.NS"
  },
  {
    "name": "PG Electroplast Limited",
    "ticker": "PGEL",
    "yf": "PGEL.NS"
  },
  {
    "name": "Procter & Gamble Hygiene and Health Care Limited",
    "ticker": "PGHH",
    "yf": "PGHH.NS"
  },
  {
    "name": "Procter & Gamble Health Limited",
    "ticker": "PGHL",
    "yf": "PGHL.NS"
  },
  {
    "name": "Pearl Global Industries Limited",
    "ticker": "PGIL",
    "yf": "PGIL.NS"
  },
  {
    "name": "The Phoenix Mills Limited",
    "ticker": "PHOENIXLTD",
    "yf": "PHOENIXLTD.NS"
  },
  {
    "name": "Piccadily Agro Industries Limited",
    "ticker": "PICCADIL",
    "yf": "PICCADIL.NS"
  },
  {
    "name": "Pidilite Industries Limited",
    "ticker": "PIDILITIND",
    "yf": "PIDILITIND.NS"
  },
  {
    "name": "Power & Instrumentation (Gujarat) Limited",
    "ticker": "PIGL",
    "yf": "PIGL.NS"
  },
  {
    "name": "PI Industries Limited",
    "ticker": "PIIND",
    "yf": "PIIND.NS"
  },
  {
    "name": "Pilani Investment and Industries Corporation Limited",
    "ticker": "PILANIINVS",
    "yf": "PILANIINVS.NS"
  },
  {
    "name": "PIL ITALICA LIFESTYLE LIMITED",
    "ticker": "PILITA",
    "yf": "PILITA.NS"
  },
  {
    "name": "Pine Labs Limited",
    "ticker": "PINELABS",
    "yf": "PINELABS.NS"
  },
  {
    "name": "Pioneer Embroideries Limited",
    "ticker": "PIONEEREMB",
    "yf": "PIONEEREMB.NS"
  },
  {
    "name": "Pioneer Investcorp Limited",
    "ticker": "PIONRINV",
    "yf": "PIONRINV.NS"
  },
  {
    "name": "Piramal Finance Limited",
    "ticker": "PIRAMALFIN",
    "yf": "PIRAMALFIN.NS"
  },
  {
    "name": "Pitti Engineering Limited",
    "ticker": "PITTIENG",
    "yf": "PITTIENG.NS"
  },
  {
    "name": "Pix Transmissions Limited",
    "ticker": "PIXTRANS",
    "yf": "PIXTRANS.NS"
  },
  {
    "name": "The Peria Karamalai Tea & Produce Company Limited",
    "ticker": "PKTEA",
    "yf": "PKTEA.NS"
  },
  {
    "name": "Plastiblends India Limited",
    "ticker": "PLASTIBLEN",
    "yf": "PLASTIBLEN.NS"
  },
  {
    "name": "Platinum Industries Limited",
    "ticker": "PLATIND",
    "yf": "PLATIND.NS"
  },
  {
    "name": "Plaza Wires Limited",
    "ticker": "PLAZACABLE",
    "yf": "PLAZACABLE.NS"
  },
  {
    "name": "Paul Merchants Limited",
    "ticker": "PML",
    "yf": "PML.NS"
  },
  {
    "name": "Punjab National Bank",
    "ticker": "PNB",
    "yf": "PNB.NS"
  },
  {
    "name": "PNB Gilts Limited",
    "ticker": "PNBGILTS",
    "yf": "PNBGILTS.NS"
  },
  {
    "name": "PNB Housing Finance Limited",
    "ticker": "PNBHOUSING",
    "yf": "PNBHOUSING.NS"
  },
  {
    "name": "PNC Infratech Limited",
    "ticker": "PNCINFRA",
    "yf": "PNCINFRA.NS"
  },
  {
    "name": "P N Gadgil Jewellers Limited",
    "ticker": "PNGJL",
    "yf": "PNGJL.NS"
  },
  {
    "name": "PNGS Reva Diamond Jewellery Limited",
    "ticker": "PNGSREVA",
    "yf": "PNGSREVA.NS"
  },
  {
    "name": "Pondy Oxides & Chemicals Limited",
    "ticker": "POCL",
    "yf": "POCL.NS"
  },
  {
    "name": "Poddar Pigments Limited",
    "ticker": "PODDARMENT",
    "yf": "PODDARMENT.NS"
  },
  {
    "name": "Pokarna Limited",
    "ticker": "POKARNA",
    "yf": "POKARNA.NS"
  },
  {
    "name": "PB Fintech Limited",
    "ticker": "POLICYBZR",
    "yf": "POLICYBZR.NS"
  },
  {
    "name": "Polycab India Limited",
    "ticker": "POLYCAB",
    "yf": "POLYCAB.NS"
  },
  {
    "name": "Poly Medicure Limited",
    "ticker": "POLYMED",
    "yf": "POLYMED.NS"
  },
  {
    "name": "Polyplex Corporation Limited",
    "ticker": "POLYPLEX",
    "yf": "POLYPLEX.NS"
  },
  {
    "name": "Ponni Sugars (Erode) Limited",
    "ticker": "PONNIERODE",
    "yf": "PONNIERODE.NS"
  },
  {
    "name": "Poonawalla Fincorp Limited",
    "ticker": "POONAWALLA",
    "yf": "POONAWALLA.NS"
  },
  {
    "name": "Power Grid Corporation of India Limited",
    "ticker": "POWERGRID",
    "yf": "POWERGRID.NS"
  },
  {
    "name": "Powerica Limited",
    "ticker": "POWERICA",
    "yf": "POWERICA.NS"
  },
  {
    "name": "Hitachi Energy India Limited",
    "ticker": "POWERINDIA",
    "yf": "POWERINDIA.NS"
  },
  {
    "name": "Power Mech Projects Limited",
    "ticker": "POWERMECH",
    "yf": "POWERMECH.NS"
  },
  {
    "name": "PPAP Automotive Limited",
    "ticker": "PPAP",
    "yf": "PPAP.NS"
  },
  {
    "name": "Prakash Pipes Limited",
    "ticker": "PPL",
    "yf": "PPL.NS"
  },
  {
    "name": "Piramal Pharma Limited",
    "ticker": "PPLPHARMA",
    "yf": "PPLPHARMA.NS"
  },
  {
    "name": "Prabha Energy Limited",
    "ticker": "PRABHA",
    "yf": "PRABHA.NS"
  },
  {
    "name": "Pradeep Metals Limited",
    "ticker": "PRADPME",
    "yf": "PRADPME.NS"
  },
  {
    "name": "Prajay Engineers Syndicate Limited",
    "ticker": "PRAENG",
    "yf": "PRAENG.NS"
  },
  {
    "name": "Praj Industries Limited",
    "ticker": "PRAJIND",
    "yf": "PRAJIND.NS"
  },
  {
    "name": "Prakash Industries Limited",
    "ticker": "PRAKASH",
    "yf": "PRAKASH.NS"
  },
  {
    "name": "Prakash Steelage Limited",
    "ticker": "PRAKASHSTL",
    "yf": "PRAKASHSTL.NS"
  },
  {
    "name": "Praveg Limited",
    "ticker": "PRAVEG",
    "yf": "PRAVEG.NS"
  },
  {
    "name": "Precision Camshafts Limited",
    "ticker": "PRECAM",
    "yf": "PRECAM.NS"
  },
  {
    "name": "Precision Wires India Limited",
    "ticker": "PRECWIRE",
    "yf": "PRECWIRE.NS"
  },
  {
    "name": "Premco Global Limited",
    "ticker": "PREMCO",
    "yf": "PREMCO.NS"
  },
  {
    "name": "Premier Explosives Limited",
    "ticker": "PREMEXPLN",
    "yf": "PREMEXPLN.NS"
  },
  {
    "name": "Premier Energies Limited",
    "ticker": "PREMIERENE",
    "yf": "PREMIERENE.NS"
  },
  {
    "name": "Prestige Estates Projects Limited",
    "ticker": "PRESTIGE",
    "yf": "PRESTIGE.NS"
  },
  {
    "name": "Pricol Limited",
    "ticker": "PRICOLLTD",
    "yf": "PRICOLLTD.NS"
  },
  {
    "name": "Prime Securities Limited",
    "ticker": "PRIMESECU",
    "yf": "PRIMESECU.NS"
  },
  {
    "name": "Primo Chemicals Limited",
    "ticker": "PRIMO",
    "yf": "PRIMO.NS"
  },
  {
    "name": "Prince Pipes And Fittings Limited",
    "ticker": "PRINCEPIPE",
    "yf": "PRINCEPIPE.NS"
  },
  {
    "name": "Pritika Auto Industries Limited",
    "ticker": "PRITIKAUTO",
    "yf": "PRITIKAUTO.NS"
  },
  {
    "name": "Privi Speciality Chemicals Limited",
    "ticker": "PRIVISCL",
    "yf": "PRIVISCL.NS"
  },
  {
    "name": "Prostarm Info Systems Limited",
    "ticker": "PROSTARM",
    "yf": "PROSTARM.NS"
  },
  {
    "name": "Protean eGov Technologies Limited",
    "ticker": "PROTEAN",
    "yf": "PROTEAN.NS"
  },
  {
    "name": "Prozone Realty Limited",
    "ticker": "PROZONER",
    "yf": "PROZONER.NS"
  },
  {
    "name": "Prism Johnson Limited",
    "ticker": "PRSMJOHNSN",
    "yf": "PRSMJOHNSN.NS"
  },
  {
    "name": "Prudent Corporate Advisory Services Limited",
    "ticker": "PRUDENT",
    "yf": "PRUDENT.NS"
  },
  {
    "name": "Prudential Sugar Corporation Limited",
    "ticker": "PRUDMOULI",
    "yf": "PRUDMOULI.NS"
  },
  {
    "name": "Punjab & Sind Bank",
    "ticker": "PSB",
    "yf": "PSB.NS"
  },
  {
    "name": "PSP Projects Limited",
    "ticker": "PSPPROJECT",
    "yf": "PSPPROJECT.NS"
  },
  {
    "name": "PTC India Limited",
    "ticker": "PTC",
    "yf": "PTC.NS"
  },
  {
    "name": "PTC Industries Limited",
    "ticker": "PTCIL",
    "yf": "PTCIL.NS"
  },
  {
    "name": "PTL Enterprises Limited",
    "ticker": "PTL",
    "yf": "PTL.NS"
  },
  {
    "name": "Punjab Chemicals & Crop Protection Limited",
    "ticker": "PUNJABCHEM",
    "yf": "PUNJABCHEM.NS"
  },
  {
    "name": "Puravankara Limited",
    "ticker": "PURVA",
    "yf": "PURVA.NS"
  },
  {
    "name": "PVP Ventures Limited",
    "ticker": "PVP",
    "yf": "PVP.NS"
  },
  {
    "name": "PVR INOX Limited",
    "ticker": "PVRINOX",
    "yf": "PVRINOX.NS"
  },
  {
    "name": "Popular Vehicles and Services Limited",
    "ticker": "PVSL",
    "yf": "PVSL.NS"
  },
  {
    "name": "Physicswallah Limited",
    "ticker": "PWL",
    "yf": "PWL.NS"
  },
  {
    "name": "Pyramid Technoplast Limited",
    "ticker": "PYRAMID",
    "yf": "PYRAMID.NS"
  },
  {
    "name": "Quality Power Electrical Equipments Limited",
    "ticker": "QPOWER",
    "yf": "QPOWER.NS"
  },
  {
    "name": "Quadrant Future Tek Limited",
    "ticker": "QUADFUTURE",
    "yf": "QUADFUTURE.NS"
  },
  {
    "name": "Quess Corp Limited",
    "ticker": "QUESS",
    "yf": "QUESS.NS"
  },
  {
    "name": "Quick Heal Technologies Limited",
    "ticker": "QUICKHEAL",
    "yf": "QUICKHEAL.NS"
  },
  {
    "name": "Quint Digital Limited",
    "ticker": "QUINT",
    "yf": "QUINT.NS"
  },
  {
    "name": "RACL Geartech Limited",
    "ticker": "RACLGEAR",
    "yf": "RACLGEAR.NS"
  },
  {
    "name": "Radaan Mediaworks India Limited",
    "ticker": "RADAAN",
    "yf": "RADAAN.NS"
  },
  {
    "name": "Radhika Jeweltech Limited",
    "ticker": "RADHIKAJWE",
    "yf": "RADHIKAJWE.NS"
  },
  {
    "name": "Radiant Cash Management Services Limited",
    "ticker": "RADIANTCMS",
    "yf": "RADIANTCMS.NS"
  },
  {
    "name": "Radico Khaitan Limited",
    "ticker": "RADICO",
    "yf": "RADICO.NS"
  },
  {
    "name": "Railtel Corporation Of India Limited",
    "ticker": "RAILTEL",
    "yf": "RAILTEL.NS"
  },
  {
    "name": "Rain Industries Limited",
    "ticker": "RAIN",
    "yf": "RAIN.NS"
  },
  {
    "name": "Rainbow Childrens Medicare Limited",
    "ticker": "RAINBOW",
    "yf": "RAINBOW.NS"
  },
  {
    "name": "Rajoo Engineers Limited",
    "ticker": "RAJOOENG",
    "yf": "RAJOOENG.NS"
  },
  {
    "name": "Rajapalayam Mills Limited",
    "ticker": "RAJPALAYAM",
    "yf": "RAJPALAYAM.NS"
  },
  {
    "name": "Rajratan Global Wire Limited",
    "ticker": "RAJRATAN",
    "yf": "RAJRATAN.NS"
  },
  {
    "name": "Rajshree Sugars & Chemicals Limited",
    "ticker": "RAJSREESUG",
    "yf": "RAJSREESUG.NS"
  },
  {
    "name": "Raj Television Network Limited",
    "ticker": "RAJTV",
    "yf": "RAJTV.NS"
  },
  {
    "name": "Rallis India Limited",
    "ticker": "RALLIS",
    "yf": "RALLIS.NS"
  },
  {
    "name": "Shree Rama Newsprint Limited",
    "ticker": "RAMANEWS",
    "yf": "RAMANEWS.NS"
  },
  {
    "name": "Rama Phosphates Limited",
    "ticker": "RAMAPHO",
    "yf": "RAMAPHO.NS"
  },
  {
    "name": "Rama Steel Tubes Limited",
    "ticker": "RAMASTEEL",
    "yf": "RAMASTEEL.NS"
  },
  {
    "name": "The Ramco Cements Limited",
    "ticker": "RAMCOCEM",
    "yf": "RAMCOCEM.NS"
  },
  {
    "name": "Ramco Industries Limited",
    "ticker": "RAMCOIND",
    "yf": "RAMCOIND.NS"
  },
  {
    "name": "Ramco Systems Limited",
    "ticker": "RAMCOSYS",
    "yf": "RAMCOSYS.NS"
  },
  {
    "name": "Ramky Infrastructure Limited",
    "ticker": "RAMKY",
    "yf": "RAMKY.NS"
  },
  {
    "name": "Ram Ratna Wires Limited",
    "ticker": "RAMRAT",
    "yf": "RAMRAT.NS"
  },
  {
    "name": "Rana Sugars Limited",
    "ticker": "RANASUG",
    "yf": "RANASUG.NS"
  },
  {
    "name": "Rane Holdings Limited",
    "ticker": "RANEHOLDIN",
    "yf": "RANEHOLDIN.NS"
  },
  {
    "name": "Rategain Travel Technologies Limited",
    "ticker": "RATEGAIN",
    "yf": "RATEGAIN.NS"
  },
  {
    "name": "Ratnamani Metals & Tubes Limited",
    "ticker": "RATNAMANI",
    "yf": "RATNAMANI.NS"
  },
  {
    "name": "Ratnaveer Precision Engineering Limited",
    "ticker": "RATNAVEER",
    "yf": "RATNAVEER.NS"
  },
  {
    "name": "Raymond Limited",
    "ticker": "RAYMOND",
    "yf": "RAYMOND.NS"
  },
  {
    "name": "Raymond Lifestyle Limited",
    "ticker": "RAYMONDLSL",
    "yf": "RAYMONDLSL.NS"
  },
  {
    "name": "Raymond Realty Limited",
    "ticker": "RAYMONDREL",
    "yf": "RAYMONDREL.NS"
  },
  {
    "name": "Restaurant Brands Asia Limited",
    "ticker": "RBA",
    "yf": "RBA.NS"
  },
  {
    "name": "RBL Bank Limited",
    "ticker": "RBLBANK",
    "yf": "RBLBANK.NS"
  },
  {
    "name": "RBZ Jewellers Limited",
    "ticker": "RBZJEWEL",
    "yf": "RBZJEWEL.NS"
  },
  {
    "name": "Rashtriya Chemicals and Fertilizers Limited",
    "ticker": "RCF",
    "yf": "RCF.NS"
  },
  {
    "name": "REC Limited",
    "ticker": "RECLTD",
    "yf": "RECLTD.NS"
  },
  {
    "name": "Redington Limited",
    "ticker": "REDINGTON",
    "yf": "REDINGTON.NS"
  },
  {
    "name": "Redtape Limited",
    "ticker": "REDTAPE",
    "yf": "REDTAPE.NS"
  },
  {
    "name": "Refex Industries Limited",
    "ticker": "REFEX",
    "yf": "REFEX.NS"
  },
  {
    "name": "Regaal Resources Limited",
    "ticker": "REGAAL",
    "yf": "REGAAL.NS"
  },
  {
    "name": "Regency Ceramics Limited",
    "ticker": "REGENCERAM",
    "yf": "REGENCERAM.NS"
  },
  {
    "name": "Relaxo Footwears Limited",
    "ticker": "RELAXO",
    "yf": "RELAXO.NS"
  },
  {
    "name": "Reliance Chemotex Industries Limited",
    "ticker": "RELCHEMQ",
    "yf": "RELCHEMQ.NS"
  },
  {
    "name": "Reliable Data Services Limited",
    "ticker": "RELIABLE",
    "yf": "RELIABLE.NS"
  },
  {
    "name": "Reliance Industries Limited",
    "ticker": "RELIANCE",
    "yf": "RELIANCE.NS"
  },
  {
    "name": "Religare Enterprises Limited",
    "ticker": "RELIGARE",
    "yf": "RELIGARE.NS"
  },
  {
    "name": "Ravindra Energy Limited",
    "ticker": "RELTD",
    "yf": "RELTD.NS"
  },
  {
    "name": "Remsons Industries Limited",
    "ticker": "REMSONSIND",
    "yf": "REMSONSIND.NS"
  },
  {
    "name": "Shree Renuka Sugars Limited",
    "ticker": "RENUKA",
    "yf": "RENUKA.NS"
  },
  {
    "name": "Repco Home Finance Limited",
    "ticker": "REPCOHOME",
    "yf": "REPCOHOME.NS"
  },
  {
    "name": "Repro India Limited",
    "ticker": "REPRO",
    "yf": "REPRO.NS"
  },
  {
    "name": "Responsive Industries Limited",
    "ticker": "RESPONIND",
    "yf": "RESPONIND.NS"
  },
  {
    "name": "JHS Svendgaard Retail Ventures Limited",
    "ticker": "RETAIL",
    "yf": "RETAIL.NS"
  },
  {
    "name": "Renaissance Global Limited",
    "ticker": "RGL",
    "yf": "RGL.NS"
  },
  {
    "name": "Rhetan TMT Limited",
    "ticker": "RHETAN",
    "yf": "RHETAN.NS"
  },
  {
    "name": "RHI MAGNESITA INDIA LIMITED",
    "ticker": "RHIM",
    "yf": "RHIM.NS"
  },
  {
    "name": "Robust Hotels Limited",
    "ticker": "RHL",
    "yf": "RHL.NS"
  },
  {
    "name": "Rico Auto Industries Limited",
    "ticker": "RICOAUTO",
    "yf": "RICOAUTO.NS"
  },
  {
    "name": "Reliance Industrial Infrastructure Limited",
    "ticker": "RIIL",
    "yf": "RIIL.NS"
  },
  {
    "name": "Rishabh Instruments Limited",
    "ticker": "RISHABH",
    "yf": "RISHABH.NS"
  },
  {
    "name": "Ritco Logistics Limited",
    "ticker": "RITCO",
    "yf": "RITCO.NS"
  },
  {
    "name": "RITES Limited",
    "ticker": "RITES",
    "yf": "RITES.NS"
  },
  {
    "name": "Ravi Kumar Distilleries Limited",
    "ticker": "RKDL",
    "yf": "RKDL.NS"
  },
  {
    "name": "RKEC Projects Limited",
    "ticker": "RKEC",
    "yf": "RKEC.NS"
  },
  {
    "name": "Ramkrishna Forgings Limited",
    "ticker": "RKFORGE",
    "yf": "RKFORGE.NS"
  },
  {
    "name": "R K Swamy Limited",
    "ticker": "RKSWAMY",
    "yf": "RKSWAMY.NS"
  },
  {
    "name": "R M Drip and Sprinklers Systems Limited",
    "ticker": "RMDRIP",
    "yf": "RMDRIP.NS"
  },
  {
    "name": "Rane (Madras) Limited",
    "ticker": "RML",
    "yf": "RML.NS"
  },
  {
    "name": "Royal Orchid Hotels Limited",
    "ticker": "ROHLTD",
    "yf": "ROHLTD.NS"
  },
  {
    "name": "Rolex Rings Limited",
    "ticker": "ROLEXRINGS",
    "yf": "ROLEXRINGS.NS"
  },
  {
    "name": "Rollatainers Limited",
    "ticker": "ROLLT",
    "yf": "ROLLT.NS"
  },
  {
    "name": "Raj Oil Mills Limited",
    "ticker": "ROML",
    "yf": "ROML.NS"
  },
  {
    "name": "Rossari Biotech Limited",
    "ticker": "ROSSARI",
    "yf": "ROSSARI.NS"
  },
  {
    "name": "Rossell India Limited",
    "ticker": "ROSSELLIND",
    "yf": "ROSSELLIND.NS"
  },
  {
    "name": "Rossell Techsys Limited",
    "ticker": "ROSSTECH",
    "yf": "ROSSTECH.NS"
  },
  {
    "name": "Roto Pumps Limited",
    "ticker": "ROTO",
    "yf": "ROTO.NS"
  },
  {
    "name": "ROUTE MOBILE LIMITED",
    "ticker": "ROUTE",
    "yf": "ROUTE.NS"
  },
  {
    "name": "Raghav Productivity Enhancers Limited",
    "ticker": "RPEL",
    "yf": "RPEL.NS"
  },
  {
    "name": "RPG Life Sciences Limited",
    "ticker": "RPGLIFE",
    "yf": "RPGLIFE.NS"
  },
  {
    "name": "Reliance Power Limited",
    "ticker": "RPOWER",
    "yf": "RPOWER.NS"
  },
  {
    "name": "R.P.P. Infra Projects Limited",
    "ticker": "RPPINFRA",
    "yf": "RPPINFRA.NS"
  },
  {
    "name": "Rajshree Polypack Limited",
    "ticker": "RPPL",
    "yf": "RPPL.NS"
  },
  {
    "name": "RPSG VENTURES LIMITED",
    "ticker": "RPSGVENT",
    "yf": "RPSGVENT.NS"
  },
  {
    "name": "Rashi Peripherals Limited",
    "ticker": "RPTECH",
    "yf": "RPTECH.NS"
  },
  {
    "name": "RRIL Limited",
    "ticker": "RRIL",
    "yf": "RRIL.NS"
  },
  {
    "name": "R R Kabel Limited",
    "ticker": "RRKABEL",
    "yf": "RRKABEL.NS"
  },
  {
    "name": "RSD Finance Limited",
    "ticker": "RSDFIN",
    "yf": "RSDFIN.NS"
  },
  {
    "name": "Rajputana Stainless Limited",
    "ticker": "RSL",
    "yf": "RSL.NS"
  },
  {
    "name": "RSWM Limited",
    "ticker": "RSWM",
    "yf": "RSWM.NS"
  },
  {
    "name": "R Systems International Limited",
    "ticker": "RSYSTEMS",
    "yf": "RSYSTEMS.NS"
  },
  {
    "name": "RattanIndia Enterprises Limited",
    "ticker": "RTNINDIA",
    "yf": "RTNINDIA.NS"
  },
  {
    "name": "RattanIndia Power Limited",
    "ticker": "RTNPOWER",
    "yf": "RTNPOWER.NS"
  },
  {
    "name": "Rubfila International Limited",
    "ticker": "RUBFILA",
    "yf": "RUBFILA.NS"
  },
  {
    "name": "Rubicon Research Limited",
    "ticker": "RUBICON",
    "yf": "RUBICON.NS"
  },
  {
    "name": "The Ruby Mills Limited",
    "ticker": "RUBYMILLS",
    "yf": "RUBYMILLS.NS"
  },
  {
    "name": "Ruchi Infrastructure Limited",
    "ticker": "RUCHINFRA",
    "yf": "RUCHINFRA.NS"
  },
  {
    "name": "Ruchira Papers Limited",
    "ticker": "RUCHIRA",
    "yf": "RUCHIRA.NS"
  },
  {
    "name": "Rupa & Company Limited",
    "ticker": "RUPA",
    "yf": "RUPA.NS"
  },
  {
    "name": "Rushil Decor Limited",
    "ticker": "RUSHIL",
    "yf": "RUSHIL.NS"
  },
  {
    "name": "Keystone Realtors Limited",
    "ticker": "RUSTOMJEE",
    "yf": "RUSTOMJEE.NS"
  },
  {
    "name": "Ravinder Heights Limited",
    "ticker": "RVHL",
    "yf": "RVHL.NS"
  },
  {
    "name": "Rail Vikas Nigam Limited",
    "ticker": "RVNL",
    "yf": "RVNL.NS"
  },
  {
    "name": "Revathi Equipment India Limited",
    "ticker": "RVTH",
    "yf": "RVTH.NS"
  },
  {
    "name": "Saatvik Green Energy Limited",
    "ticker": "SAATVIKGL",
    "yf": "SAATVIKGL.NS"
  },
  {
    "name": "Sadbhav Infrastructure Project Limited",
    "ticker": "SADBHIN",
    "yf": "SADBHIN.NS"
  },
  {
    "name": "Safari Industries (India) Limited",
    "ticker": "SAFARI",
    "yf": "SAFARI.NS"
  },
  {
    "name": "Sagardeep Alloys Limited",
    "ticker": "SAGARDEEP",
    "yf": "SAGARDEEP.NS"
  },
  {
    "name": "Sagar Cements Limited",
    "ticker": "SAGCEM",
    "yf": "SAGCEM.NS"
  },
  {
    "name": "SAGILITY LIMITED",
    "ticker": "SAGILITY",
    "yf": "SAGILITY.NS"
  },
  {
    "name": "Shalibhadra Finance Limited",
    "ticker": "SAHLIBHFI",
    "yf": "SAHLIBHFI.NS"
  },
  {
    "name": "Sahyadri Industries Limited",
    "ticker": "SAHYADRI",
    "yf": "SAHYADRI.NS"
  },
  {
    "name": "Steel Authority of India Limited",
    "ticker": "SAIL",
    "yf": "SAIL.NS"
  },
  {
    "name": "Sai Life Sciences Limited",
    "ticker": "SAILIFE",
    "yf": "SAILIFE.NS"
  },
  {
    "name": "Sai Parenterals Limited",
    "ticker": "SAIPARENT",
    "yf": "SAIPARENT.NS"
  },
  {
    "name": "Sakar Healthcare Limited",
    "ticker": "SAKAR",
    "yf": "SAKAR.NS"
  },
  {
    "name": "Sakthi Sugars Limited",
    "ticker": "SAKHTISUG",
    "yf": "SAKHTISUG.NS"
  },
  {
    "name": "Saksoft Limited",
    "ticker": "SAKSOFT",
    "yf": "SAKSOFT.NS"
  },
  {
    "name": "Salasar Techno Engineering Limited",
    "ticker": "SALASAR",
    "yf": "SALASAR.NS"
  },
  {
    "name": "Salona Cotspin Limited",
    "ticker": "SALONA",
    "yf": "SALONA.NS"
  },
  {
    "name": "S.A.L. Steel Limited",
    "ticker": "SALSTEEL",
    "yf": "SALSTEEL.NS"
  },
  {
    "name": "Salzer Electronics Limited",
    "ticker": "SALZERELEC",
    "yf": "SALZERELEC.NS"
  },
  {
    "name": "Sambhv Steel Tubes Limited",
    "ticker": "SAMBHV",
    "yf": "SAMBHV.NS"
  },
  {
    "name": "Samhi Hotels Limited",
    "ticker": "SAMHI",
    "yf": "SAMHI.NS"
  },
  {
    "name": "Sammaan Capital Limited",
    "ticker": "SAMMAANCAP",
    "yf": "SAMMAANCAP.NS"
  },
  {
    "name": "Sampann Utpadan India Limited",
    "ticker": "SAMPANN",
    "yf": "SAMPANN.NS"
  },
  {
    "name": "Sanathan Textiles Limited",
    "ticker": "SANATHAN",
    "yf": "SANATHAN.NS"
  },
  {
    "name": "The Sandesh Limited",
    "ticker": "SANDESH",
    "yf": "SANDESH.NS"
  },
  {
    "name": "Sandhar Technologies Limited",
    "ticker": "SANDHAR",
    "yf": "SANDHAR.NS"
  },
  {
    "name": "Sandur Manganese & Iron Ores Limited",
    "ticker": "SANDUMA",
    "yf": "SANDUMA.NS"
  },
  {
    "name": "Sangam (India) Limited",
    "ticker": "SANGAMIND",
    "yf": "SANGAMIND.NS"
  },
  {
    "name": "Sanghvi Movers Limited",
    "ticker": "SANGHVIMOV",
    "yf": "SANGHVIMOV.NS"
  },
  {
    "name": "Sanofi India Limited",
    "ticker": "SANOFI",
    "yf": "SANOFI.NS"
  },
  {
    "name": "Sanofi Consumer Healthcare India Limited",
    "ticker": "SANOFICONR",
    "yf": "SANOFICONR.NS"
  },
  {
    "name": "Sansera Engineering Limited",
    "ticker": "SANSERA",
    "yf": "SANSERA.NS"
  },
  {
    "name": "Sanstar Limited",
    "ticker": "SANSTAR",
    "yf": "SANSTAR.NS"
  },
  {
    "name": "Sapphire Foods India Limited",
    "ticker": "SAPPHIRE",
    "yf": "SAPPHIRE.NS"
  },
  {
    "name": "Shree Ajit Pulp & Paper Limited",
    "ticker": "SAPPL",
    "yf": "SAPPL.NS"
  },
  {
    "name": "Sarda Energy & Minerals Limited",
    "ticker": "SARDAEN",
    "yf": "SARDAEN.NS"
  },
  {
    "name": "Saregama India Limited",
    "ticker": "SAREGAMA",
    "yf": "SAREGAMA.NS"
  },
  {
    "name": "Sarla Performance Fibers Limited",
    "ticker": "SARLAPOLY",
    "yf": "SARLAPOLY.NS"
  },
  {
    "name": "Sasken Technologies Limited",
    "ticker": "SASKEN",
    "yf": "SASKEN.NS"
  },
  {
    "name": "Satia Industries Limited",
    "ticker": "SATIA",
    "yf": "SATIA.NS"
  },
  {
    "name": "Satin Creditcare Network Limited",
    "ticker": "SATIN",
    "yf": "SATIN.NS"
  },
  {
    "name": "Saurashtra Cement Limited",
    "ticker": "SAURASHCEM",
    "yf": "SAURASHCEM.NS"
  },
  {
    "name": "Sayaji Hotels Limited",
    "ticker": "SAYAJIHOTL",
    "yf": "SAYAJIHOTL.NS"
  },
  {
    "name": "SBC Exports Limited",
    "ticker": "SBC",
    "yf": "SBC.NS"
  },
  {
    "name": "Shivalik Bimetal Controls Limited",
    "ticker": "SBCL",
    "yf": "SBCL.NS"
  },
  {
    "name": "SBFC Finance Limited",
    "ticker": "SBFC",
    "yf": "SBFC.NS"
  },
  {
    "name": "Suratwwala Business Group Limited",
    "ticker": "SBGLP",
    "yf": "SBGLP.NS"
  },
  {
    "name": "SBI Cards and Payment Services Limited",
    "ticker": "SBICARD",
    "yf": "SBICARD.NS"
  },
  {
    "name": "SBI Life Insurance Company Limited",
    "ticker": "SBILIFE",
    "yf": "SBILIFE.NS"
  },
  {
    "name": "State Bank of India",
    "ticker": "SBIN",
    "yf": "SBIN.NS"
  },
  {
    "name": "Scan Steels Limited",
    "ticker": "SCANSTL",
    "yf": "SCANSTL.NS"
  },
  {
    "name": "Schaeffler India Limited",
    "ticker": "SCHAEFFLER",
    "yf": "SCHAEFFLER.NS"
  },
  {
    "name": "S Chand And Company Limited",
    "ticker": "SCHAND",
    "yf": "SCHAND.NS"
  },
  {
    "name": "Shipping Corporation Of India Limited",
    "ticker": "SCI",
    "yf": "SCI.NS"
  },
  {
    "name": "Shipping Corporation of India Land and Assets Limited",
    "ticker": "SCILAL",
    "yf": "SCILAL.NS"
  },
  {
    "name": "Scoda Tubes Limited",
    "ticker": "SCODATUBES",
    "yf": "SCODATUBES.NS"
  },
  {
    "name": "Som Distilleries & Breweries Limited",
    "ticker": "SDBL",
    "yf": "SDBL.NS"
  },
  {
    "name": "Seamec Limited",
    "ticker": "SEAMECLTD",
    "yf": "SEAMECLTD.NS"
  },
  {
    "name": "SEDEMAC Mechatronics Limited",
    "ticker": "SEDEMAC",
    "yf": "SEDEMAC.NS"
  },
  {
    "name": "Shanti Educational Initiatives Limited",
    "ticker": "SEIL",
    "yf": "SEIL.NS"
  },
  {
    "name": "SEL Manufacturing Company Limited",
    "ticker": "SELMC",
    "yf": "SELMC.NS"
  },
  {
    "name": "Semac Construction Limited",
    "ticker": "SEMAC",
    "yf": "SEMAC.NS"
  },
  {
    "name": "Senco Gold Limited",
    "ticker": "SENCO",
    "yf": "SENCO.NS"
  },
  {
    "name": "Senores Pharmaceuticals Limited",
    "ticker": "SENORES",
    "yf": "SENORES.NS"
  },
  {
    "name": "SEPC Limited",
    "ticker": "SEPC",
    "yf": "SEPC.NS"
  },
  {
    "name": "Servotech Renewable Power System Limited",
    "ticker": "SERVOTECH",
    "yf": "SERVOTECH.NS"
  },
  {
    "name": "Seshasayee Paper and Boards Limited",
    "ticker": "SESHAPAPER",
    "yf": "SESHAPAPER.NS"
  },
  {
    "name": "Standard Engineering Technology Limited",
    "ticker": "SETL",
    "yf": "SETL.NS"
  },
  {
    "name": "Sheela Foam Limited",
    "ticker": "SFL",
    "yf": "SFL.NS"
  },
  {
    "name": "SG Finserve Limited",
    "ticker": "SGFIN",
    "yf": "SGFIN.NS"
  },
  {
    "name": "Synergy Green Industries Limited",
    "ticker": "SGIL",
    "yf": "SGIL.NS"
  },
  {
    "name": "STL Global Limited",
    "ticker": "SGL",
    "yf": "SGL.NS"
  },
  {
    "name": "SG Mart Limited",
    "ticker": "SGMART",
    "yf": "SGMART.NS"
  },
  {
    "name": "Shadowfax Technologies Limited",
    "ticker": "SHADOWFAX",
    "yf": "SHADOWFAX.NS"
  },
  {
    "name": "Shah Metacorp Limited",
    "ticker": "SHAH",
    "yf": "SHAH.NS"
  },
  {
    "name": "Shah Alloys Limited",
    "ticker": "SHAHALLOYS",
    "yf": "SHAHALLOYS.NS"
  },
  {
    "name": "Shaily Engineering Plastics Limited",
    "ticker": "SHAILY",
    "yf": "SHAILY.NS"
  },
  {
    "name": "Shakti Pumps (India) Limited",
    "ticker": "SHAKTIPUMP",
    "yf": "SHAKTIPUMP.NS"
  },
  {
    "name": "Shalby Limited",
    "ticker": "SHALBY",
    "yf": "SHALBY.NS"
  },
  {
    "name": "Shalimar Paints Limited",
    "ticker": "SHALPAINTS",
    "yf": "SHALPAINTS.NS"
  },
  {
    "name": "Shanti Overseas (India) Limited",
    "ticker": "SHANTI",
    "yf": "SHANTI.NS"
  },
  {
    "name": "Shanthi Gears Limited",
    "ticker": "SHANTIGEAR",
    "yf": "SHANTIGEAR.NS"
  },
  {
    "name": "Shanti Gold International Limited",
    "ticker": "SHANTIGOLD",
    "yf": "SHANTIGOLD.NS"
  },
  {
    "name": "Sharda Cropchem Limited",
    "ticker": "SHARDACROP",
    "yf": "SHARDACROP.NS"
  },
  {
    "name": "Sharda Motor Industries Limited",
    "ticker": "SHARDAMOTR",
    "yf": "SHARDAMOTR.NS"
  },
  {
    "name": "Shardul Securities Limited",
    "ticker": "SHARDUL",
    "yf": "SHARDUL.NS"
  },
  {
    "name": "Share India Securities Limited",
    "ticker": "SHAREINDIA",
    "yf": "SHAREINDIA.NS"
  },
  {
    "name": "Shri Bajrang Alliance Limited",
    "ticker": "SHBAJRG",
    "yf": "SHBAJRG.NS"
  },
  {
    "name": "Shemaroo Entertainment Limited",
    "ticker": "SHEMAROO",
    "yf": "SHEMAROO.NS"
  },
  {
    "name": "Shilchar Technologies Limited",
    "ticker": "SHILCTECH",
    "yf": "SHILCTECH.NS"
  },
  {
    "name": "Shilpa Medicare Limited",
    "ticker": "SHILPAMED",
    "yf": "SHILPAMED.NS"
  },
  {
    "name": "Sharat Industries Limited",
    "ticker": "SHINDL",
    "yf": "SHINDL.NS"
  },
  {
    "name": "Shivalik Rasayan Limited",
    "ticker": "SHIVALIK",
    "yf": "SHIVALIK.NS"
  },
  {
    "name": "Shiva Mills Limited",
    "ticker": "SHIVAMILLS",
    "yf": "SHIVAMILLS.NS"
  },
  {
    "name": "Shiva Texyarn Limited",
    "ticker": "SHIVATEX",
    "yf": "SHIVATEX.NS"
  },
  {
    "name": "S H Kelkar and Company Limited",
    "ticker": "SHK",
    "yf": "SHK.NS"
  },
  {
    "name": "Shoppers Stop Limited",
    "ticker": "SHOPERSTOP",
    "yf": "SHOPERSTOP.NS"
  },
  {
    "name": "Shradha Realty Limited",
    "ticker": "SHRADHA",
    "yf": "SHRADHA.NS"
  },
  {
    "name": "Shree Digvijay Cement Co.Ltd",
    "ticker": "SHREDIGCEM",
    "yf": "SHREDIGCEM.NS"
  },
  {
    "name": "SHREE CEMENT LIMITED",
    "ticker": "SHREECEM",
    "yf": "SHREECEM.NS"
  },
  {
    "name": "Shreeji Shipping Global Limited",
    "ticker": "SHREEJISPG",
    "yf": "SHREEJISPG.NS"
  },
  {
    "name": "Shree Pushkar Chemicals & Fertilisers Limited",
    "ticker": "SHREEPUSHK",
    "yf": "SHREEPUSHK.NS"
  },
  {
    "name": "Shree Rama Multi-Tech Limited",
    "ticker": "SHREERAMA",
    "yf": "SHREERAMA.NS"
  },
  {
    "name": "Shreyans Industries Limited",
    "ticker": "SHREYANIND",
    "yf": "SHREYANIND.NS"
  },
  {
    "name": "Shri Krishna Devcon Limited",
    "ticker": "SHRIKRISH",
    "yf": "SHRIKRISH.NS"
  },
  {
    "name": "Shringar House of Mangalsutra Limited",
    "ticker": "SHRINGARMS",
    "yf": "SHRINGARMS.NS"
  },
  {
    "name": "Shriram Pistons & Rings Limited",
    "ticker": "SHRIPISTON",
    "yf": "SHRIPISTON.NS"
  },
  {
    "name": "Shriram Finance Limited",
    "ticker": "SHRIRAMFIN",
    "yf": "SHRIRAMFIN.NS"
  },
  {
    "name": "Shriram Properties Limited",
    "ticker": "SHRIRAMPPS",
    "yf": "SHRIRAMPPS.NS"
  },
  {
    "name": "Shyam Century Ferrous Limited",
    "ticker": "SHYAMCENT",
    "yf": "SHYAMCENT.NS"
  },
  {
    "name": "Shyam Metalics and Energy Limited",
    "ticker": "SHYAMMETL",
    "yf": "SHYAMMETL.NS"
  },
  {
    "name": "Sicagen India Limited",
    "ticker": "SICAGEN",
    "yf": "SICAGEN.NS"
  },
  {
    "name": "Siemens Limited",
    "ticker": "SIEMENS",
    "yf": "SIEMENS.NS"
  },
  {
    "name": "Signet Industries Limited",
    "ticker": "SIGIND",
    "yf": "SIGIND.NS"
  },
  {
    "name": "Sigma Solve Limited",
    "ticker": "SIGMA",
    "yf": "SIGMA.NS"
  },
  {
    "name": "Signatureglobal (India) Limited",
    "ticker": "SIGNATURE",
    "yf": "SIGNATURE.NS"
  },
  {
    "name": "Signpost India Limited",
    "ticker": "SIGNPOST",
    "yf": "SIGNPOST.NS"
  },
  {
    "name": "Sika Interplant Systems Limited",
    "ticker": "SIKA",
    "yf": "SIKA.NS"
  },
  {
    "name": "Sikko Industries Limited",
    "ticker": "SIKKO",
    "yf": "SIKKO.NS"
  },
  {
    "name": "Standard Industries Limited",
    "ticker": "SIL",
    "yf": "SIL.NS"
  },
  {
    "name": "Silgo Retail Limited",
    "ticker": "SILGO",
    "yf": "SILGO.NS"
  },
  {
    "name": "SIL Investments Limited",
    "ticker": "SILINV",
    "yf": "SILINV.NS"
  },
  {
    "name": "Silly Monks Entertainment Limited",
    "ticker": "SILLYMONKS",
    "yf": "SILLYMONKS.NS"
  },
  {
    "name": "Silver Touch Technologies Limited",
    "ticker": "SILVERTUC",
    "yf": "SILVERTUC.NS"
  },
  {
    "name": "Simplex Infrastructures Limited",
    "ticker": "SIMPLEXINF",
    "yf": "SIMPLEXINF.NS"
  },
  {
    "name": "Sinclairs Hotels Limited",
    "ticker": "SINCLAIR",
    "yf": "SINCLAIR.NS"
  },
  {
    "name": "Sindhu Trade Links Limited",
    "ticker": "SINDHUTRAD",
    "yf": "SINDHUTRAD.NS"
  },
  {
    "name": "Singer India Limited",
    "ticker": "SINGERIND",
    "yf": "SINGERIND.NS"
  },
  {
    "name": "Sintercom India Limited",
    "ticker": "SINTERCOM",
    "yf": "SINTERCOM.NS"
  },
  {
    "name": "Sirca Paints India Limited",
    "ticker": "SIRCA",
    "yf": "SIRCA.NS"
  },
  {
    "name": "SIS LIMITED",
    "ticker": "SIS",
    "yf": "SIS.NS"
  },
  {
    "name": "Siyaram Silk Mills Limited",
    "ticker": "SIYSIL",
    "yf": "SIYSIL.NS"
  },
  {
    "name": "S.J.S. Enterprises Limited",
    "ticker": "SJS",
    "yf": "SJS.NS"
  },
  {
    "name": "SJVN Limited",
    "ticker": "SJVN",
    "yf": "SJVN.NS"
  },
  {
    "name": "SKF India Limited",
    "ticker": "SKFINDIA",
    "yf": "SKFINDIA.NS"
  },
  {
    "name": "SKF India (Industrial) Limited",
    "ticker": "SKFINDUS",
    "yf": "SKFINDUS.NS"
  },
  {
    "name": "Skipper Limited",
    "ticker": "SKIPPER",
    "yf": "SKIPPER.NS"
  },
  {
    "name": "SKM Egg Products Export (India) Limited",
    "ticker": "SKMEGGPROD",
    "yf": "SKMEGGPROD.NS"
  },
  {
    "name": "SKY GOLD AND DIAMONDS LIMITED",
    "ticker": "SKYGOLD",
    "yf": "SKYGOLD.NS"
  },
  {
    "name": "Smartlink Holdings Limited",
    "ticker": "SMARTLINK",
    "yf": "SMARTLINK.NS"
  },
  {
    "name": "Smartworks Coworking Spaces Limited",
    "ticker": "SMARTWORKS",
    "yf": "SMARTWORKS.NS"
  },
  {
    "name": "SMC Global Securities Limited",
    "ticker": "SMCGLOBAL",
    "yf": "SMCGLOBAL.NS"
  },
  {
    "name": "SML Mahindra Limited",
    "ticker": "SMLMAH",
    "yf": "SMLMAH.NS"
  },
  {
    "name": "Sarthak Metals Limited",
    "ticker": "SMLT",
    "yf": "SMLT.NS"
  },
  {
    "name": "SMS Pharmaceuticals Limited",
    "ticker": "SMSPHARMA",
    "yf": "SMSPHARMA.NS"
  },
  {
    "name": "Snowman Logistics Limited",
    "ticker": "SNOWMAN",
    "yf": "SNOWMAN.NS"
  },
  {
    "name": "Sobha Limited",
    "ticker": "SOBHA",
    "yf": "SOBHA.NS"
  },
  {
    "name": "Solara Active Pharma Sciences Limited",
    "ticker": "SOLARA",
    "yf": "SOLARA.NS"
  },
  {
    "name": "Solar Industries India Limited",
    "ticker": "SOLARINDS",
    "yf": "SOLARINDS.NS"
  },
  {
    "name": "Solarworld Energy Solutions Limited",
    "ticker": "SOLARWORLD",
    "yf": "SOLARWORLD.NS"
  },
  {
    "name": "Solex Energy Limited",
    "ticker": "SOLEX",
    "yf": "SOLEX.NS"
  },
  {
    "name": "Somany Ceramics Limited",
    "ticker": "SOMANYCERA",
    "yf": "SOMANYCERA.NS"
  },
  {
    "name": "Soma Textiles & Industries Limited",
    "ticker": "SOMATEX",
    "yf": "SOMATEX.NS"
  },
  {
    "name": "Somi Conveyor Beltings Limited",
    "ticker": "SOMICONVEY",
    "yf": "SOMICONVEY.NS"
  },
  {
    "name": "Sona BLW Precision Forgings Limited",
    "ticker": "SONACOMS",
    "yf": "SONACOMS.NS"
  },
  {
    "name": "Sonal Mercantile Limited",
    "ticker": "SONAL",
    "yf": "SONAL.NS"
  },
  {
    "name": "SONAM LIMITED",
    "ticker": "SONAMLTD",
    "yf": "SONAMLTD.NS"
  },
  {
    "name": "Sonata Software Limited",
    "ticker": "SONATSOFTW",
    "yf": "SONATSOFTW.NS"
  },
  {
    "name": "Savita Oil Technologies Limited",
    "ticker": "SOTL",
    "yf": "SOTL.NS"
  },
  {
    "name": "The South Indian Bank Limited",
    "ticker": "SOUTHBANK",
    "yf": "SOUTHBANK.NS"
  },
  {
    "name": "South West Pinnacle Exploration Limited",
    "ticker": "SOUTHWEST",
    "yf": "SOUTHWEST.NS"
  },
  {
    "name": "S. P. Apparels Limited",
    "ticker": "SPAL",
    "yf": "SPAL.NS"
  },
  {
    "name": "Spandana Sphoorty Financial Limited",
    "ticker": "SPANDANA",
    "yf": "SPANDANA.NS"
  },
  {
    "name": "Sun Pharma Advanced Research Company Limited",
    "ticker": "SPARC",
    "yf": "SPARC.NS"
  },
  {
    "name": "Spacenet Enterprises India Limited",
    "ticker": "SPCENET",
    "yf": "SPCENET.NS"
  },
  {
    "name": "Speciality Restaurants Limited",
    "ticker": "SPECIALITY",
    "yf": "SPECIALITY.NS"
  },
  {
    "name": "Spectrum Electrical Industries Limited",
    "ticker": "SPECTRUM",
    "yf": "SPECTRUM.NS"
  },
  {
    "name": "Spencer's Retail Limited",
    "ticker": "SPENCERS",
    "yf": "SPENCERS.NS"
  },
  {
    "name": "Southern Petrochemicals Industries Corporation  Limited",
    "ticker": "SPIC",
    "yf": "SPIC.NS"
  },
  {
    "name": "SPL Industries Limited",
    "ticker": "SPLIL",
    "yf": "SPLIL.NS"
  },
  {
    "name": "Supreme Petrochem Limited",
    "ticker": "SPLPETRO",
    "yf": "SPLPETRO.NS"
  },
  {
    "name": "SPML Infra Limited",
    "ticker": "SPMLINFRA",
    "yf": "SPMLINFRA.NS"
  },
  {
    "name": "Sportking India Limited",
    "ticker": "SPORTKING",
    "yf": "SPORTKING.NS"
  },
  {
    "name": "Shankar Lal Rampal Dye-Chem Limited",
    "ticker": "SRD",
    "yf": "SRD.NS"
  },
  {
    "name": "Sreeleathers Limited",
    "ticker": "SREEL",
    "yf": "SREEL.NS"
  },
  {
    "name": "SRF Limited",
    "ticker": "SRF",
    "yf": "SRF.NS"
  },
  {
    "name": "SRG Housing Finance Limited",
    "ticker": "SRGHFL",
    "yf": "SRGHFL.NS"
  },
  {
    "name": "Sree Rayalaseema Hi-Strength Hypo Limited",
    "ticker": "SRHHYPOLTD",
    "yf": "SRHHYPOLTD.NS"
  },
  {
    "name": "SRM Contractors Limited",
    "ticker": "SRM",
    "yf": "SRM.NS"
  },
  {
    "name": "Shree Ram Twistex Limited",
    "ticker": "SRTL",
    "yf": "SRTL.NS"
  },
  {
    "name": "Saraswati Saree Depot Limited",
    "ticker": "SSDL",
    "yf": "SSDL.NS"
  },
  {
    "name": "Steel Strips Wheels Limited",
    "ticker": "SSWL",
    "yf": "SSWL.NS"
  },
  {
    "name": "Stallion India Fluorochemicals Limited",
    "ticker": "STALLION",
    "yf": "STALLION.NS"
  },
  {
    "name": "Stanley Lifestyles Limited",
    "ticker": "STANLEY",
    "yf": "STANLEY.NS"
  },
  {
    "name": "Strides Pharma Science Limited",
    "ticker": "STAR",
    "yf": "STAR.NS"
  },
  {
    "name": "Star Cement Limited",
    "ticker": "STARCEMENT",
    "yf": "STARCEMENT.NS"
  },
  {
    "name": "Star Health and Allied Insurance Company Limited",
    "ticker": "STARHEALTH",
    "yf": "STARHEALTH.NS"
  },
  {
    "name": "Star Paper Mills Limited",
    "ticker": "STARPAPER",
    "yf": "STARPAPER.NS"
  },
  {
    "name": "Starteck Finance Limited",
    "ticker": "STARTECK",
    "yf": "STARTECK.NS"
  },
  {
    "name": "The State Trading Corporation of India Limited",
    "ticker": "STCINDIA",
    "yf": "STCINDIA.NS"
  },
  {
    "name": "Steelcast Limited",
    "ticker": "STEELCAS",
    "yf": "STEELCAS.NS"
  },
  {
    "name": "Steel City Securities Limited",
    "ticker": "STEELCITY",
    "yf": "STEELCITY.NS"
  },
  {
    "name": "STEEL EXCHANGE INDIA LIMITED",
    "ticker": "STEELXIND",
    "yf": "STEELXIND.NS"
  },
  {
    "name": "Stel Holdings Limited",
    "ticker": "STEL",
    "yf": "STEL.NS"
  },
  {
    "name": "Sterling Tools Limited",
    "ticker": "STERTOOLS",
    "yf": "STERTOOLS.NS"
  },
  {
    "name": "STL Networks Limited",
    "ticker": "STLNETWORK",
    "yf": "STLNETWORK.NS"
  },
  {
    "name": "Sterlite Technologies Limited",
    "ticker": "STLTECH",
    "yf": "STLTECH.NS"
  },
  {
    "name": "Stove Kraft Limited",
    "ticker": "STOVEKRAFT",
    "yf": "STOVEKRAFT.NS"
  },
  {
    "name": "Studds Accessories Limited",
    "ticker": "STUDDS",
    "yf": "STUDDS.NS"
  },
  {
    "name": "Seshaasai Technologies Limited",
    "ticker": "STYL",
    "yf": "STYL.NS"
  },
  {
    "name": "Stylam Industries Limited",
    "ticker": "STYLAMIND",
    "yf": "STYLAMIND.NS"
  },
  {
    "name": "Baazar Style Retail Limited",
    "ticker": "STYLEBAAZA",
    "yf": "STYLEBAAZA.NS"
  },
  {
    "name": "Styrenix Performance Materials Limited",
    "ticker": "STYRENIX",
    "yf": "STYRENIX.NS"
  },
  {
    "name": "Subex Limited",
    "ticker": "SUBEXLTD",
    "yf": "SUBEXLTD.NS"
  },
  {
    "name": "Subros Limited",
    "ticker": "SUBROS",
    "yf": "SUBROS.NS"
  },
  {
    "name": "Sudarshan Colorants India Limited",
    "ticker": "SUDARCOLOR",
    "yf": "SUDARCOLOR.NS"
  },
  {
    "name": "Sudarshan Chemical Industries Limited",
    "ticker": "SUDARSCHEM",
    "yf": "SUDARSCHEM.NS"
  },
  {
    "name": "Sudeep Pharma Limited",
    "ticker": "SUDEEPPHRM",
    "yf": "SUDEEPPHRM.NS"
  },
  {
    "name": "Sukhjit Starch & Chemicals Limited",
    "ticker": "SUKHJITS",
    "yf": "SUKHJITS.NS"
  },
  {
    "name": "Sula Vineyards Limited",
    "ticker": "SULA",
    "yf": "SULA.NS"
  },
  {
    "name": "Sumeet Industries Limited",
    "ticker": "SUMEETINDS",
    "yf": "SUMEETINDS.NS"
  },
  {
    "name": "Sumitomo Chemical India Limited",
    "ticker": "SUMICHEM",
    "yf": "SUMICHEM.NS"
  },
  {
    "name": "Summit Securities Limited",
    "ticker": "SUMMITSEC",
    "yf": "SUMMITSEC.NS"
  },
  {
    "name": "Sundaram Clayton Limited",
    "ticker": "SUNCLAY",
    "yf": "SUNCLAY.NS"
  },
  {
    "name": "Sundaram Multi Pap Limited",
    "ticker": "SUNDARAM",
    "yf": "SUNDARAM.NS"
  },
  {
    "name": "Sundaram Finance Limited",
    "ticker": "SUNDARMFIN",
    "yf": "SUNDARMFIN.NS"
  },
  {
    "name": "Sundaram Brake Linings Limited",
    "ticker": "SUNDRMBRAK",
    "yf": "SUNDRMBRAK.NS"
  },
  {
    "name": "Sundram Fasteners Limited",
    "ticker": "SUNDRMFAST",
    "yf": "SUNDRMFAST.NS"
  },
  {
    "name": "Sundrop Brands Limited",
    "ticker": "SUNDROP",
    "yf": "SUNDROP.NS"
  },
  {
    "name": "Sunflag Iron And Steel Company Limited",
    "ticker": "SUNFLAG",
    "yf": "SUNFLAG.NS"
  },
  {
    "name": "Sun Pharmaceutical Industries Limited",
    "ticker": "SUNPHARMA",
    "yf": "SUNPHARMA.NS"
  },
  {
    "name": "Sunteck Realty Limited",
    "ticker": "SUNTECK",
    "yf": "SUNTECK.NS"
  },
  {
    "name": "Sun TV Network Limited",
    "ticker": "SUNTV",
    "yf": "SUNTV.NS"
  },
  {
    "name": "Superhouse Limited",
    "ticker": "SUPERHOUSE",
    "yf": "SUPERHOUSE.NS"
  },
  {
    "name": "Super Spinning Mills Limited",
    "ticker": "SUPERSPIN",
    "yf": "SUPERSPIN.NS"
  },
  {
    "name": "Suprajit Engineering Limited",
    "ticker": "SUPRAJIT",
    "yf": "SUPRAJIT.NS"
  },
  {
    "name": "Supreme Holdings & Hospitality (India) Limited",
    "ticker": "SUPREME",
    "yf": "SUPREME.NS"
  },
  {
    "name": "Supreme Industries Limited",
    "ticker": "SUPREMEIND",
    "yf": "SUPREMEIND.NS"
  },
  {
    "name": "Supriya Lifescience Limited",
    "ticker": "SUPRIYA",
    "yf": "SUPRIYA.NS"
  },
  {
    "name": "Suraj Estate Developers Limited",
    "ticker": "SURAJEST",
    "yf": "SURAJEST.NS"
  },
  {
    "name": "Suraj Limited",
    "ticker": "SURAJLTD",
    "yf": "SURAJLTD.NS"
  },
  {
    "name": "Suraksha Diagnostic Limited",
    "ticker": "SURAKSHA",
    "yf": "SURAKSHA.NS"
  },
  {
    "name": "Surana Solar Limited",
    "ticker": "SURANASOL",
    "yf": "SURANASOL.NS"
  },
  {
    "name": "Surana Telecom and Power Limited",
    "ticker": "SURANAT&P",
    "yf": "SURANAT&P.NS"
  },
  {
    "name": "Suryalata Spinning Mills Limited",
    "ticker": "SURYALA",
    "yf": "SURYALA.NS"
  },
  {
    "name": "Suryalakshmi Cotton Mills Limited",
    "ticker": "SURYALAXMI",
    "yf": "SURYALAXMI.NS"
  },
  {
    "name": "Surya Roshni Limited",
    "ticker": "SURYAROSNI",
    "yf": "SURYAROSNI.NS"
  },
  {
    "name": "Suryoday Small Finance Bank Limited",
    "ticker": "SURYODAY",
    "yf": "SURYODAY.NS"
  },
  {
    "name": "Sutlej Textiles and Industries Limited",
    "ticker": "SUTLEJTEX",
    "yf": "SUTLEJTEX.NS"
  },
  {
    "name": "Suven Life Sciences Limited",
    "ticker": "SUVEN",
    "yf": "SUVEN.NS"
  },
  {
    "name": "Suyog Telematics Limited",
    "ticker": "SUYOG",
    "yf": "SUYOG.NS"
  },
  {
    "name": "Suzlon Energy Limited",
    "ticker": "SUZLON",
    "yf": "SUZLON.NS"
  },
  {
    "name": "Shree Vasu Logistics Limited",
    "ticker": "SVLL",
    "yf": "SVLL.NS"
  },
  {
    "name": "SVP GLOBAL TEXTILES LIMITED",
    "ticker": "SVPGLOB",
    "yf": "SVPGLOB.NS"
  },
  {
    "name": "SWAN CORP LIMITED",
    "ticker": "SWANCORP",
    "yf": "SWANCORP.NS"
  },
  {
    "name": "Swaraj Engines Limited",
    "ticker": "SWARAJENG",
    "yf": "SWARAJENG.NS"
  },
  {
    "name": "Swelect Energy Systems Limited",
    "ticker": "SWELECTES",
    "yf": "SWELECTES.NS"
  },
  {
    "name": "Swiggy Limited",
    "ticker": "SWIGGY",
    "yf": "SWIGGY.NS"
  },
  {
    "name": "Sterling and Wilson Renewable Energy Limited",
    "ticker": "SWSOLAR",
    "yf": "SWSOLAR.NS"
  },
  {
    "name": "Symphony Limited",
    "ticker": "SYMPHONY",
    "yf": "SYMPHONY.NS"
  },
  {
    "name": "Syncom Formulations (India) Limited",
    "ticker": "SYNCOMF",
    "yf": "SYNCOMF.NS"
  },
  {
    "name": "Syngene International Limited",
    "ticker": "SYNGENE",
    "yf": "SYNGENE.NS"
  },
  {
    "name": "Syrma SGS Technology Limited",
    "ticker": "SYRMA",
    "yf": "SYRMA.NS"
  },
  {
    "name": "Systematix Corporate Services Limited",
    "ticker": "SYSTMTXC",
    "yf": "SYSTMTXC.NS"
  },
  {
    "name": "Taal Tech Limited",
    "ticker": "TAALTECH",
    "yf": "TAALTECH.NS"
  },
  {
    "name": "Tainwala Chemical and Plastic (I) Limited",
    "ticker": "TAINWALCHM",
    "yf": "TAINWALCHM.NS"
  },
  {
    "name": "Taj GVK Hotels & Resorts Limited",
    "ticker": "TAJGVK",
    "yf": "TAJGVK.NS"
  },
  {
    "name": "Talbros Automotive Components Limited",
    "ticker": "TALBROAUTO",
    "yf": "TALBROAUTO.NS"
  },
  {
    "name": "Tamboli Industries Limited",
    "ticker": "TAMBOLIIN",
    "yf": "TAMBOLIIN.NS"
  },
  {
    "name": "Tanla Platforms Limited",
    "ticker": "TANLA",
    "yf": "TANLA.NS"
  },
  {
    "name": "Tara Chand InfraLogistic Solutions Limited",
    "ticker": "TARACHAND",
    "yf": "TARACHAND.NS"
  },
  {
    "name": "Tarapur Transformers Limited",
    "ticker": "TARAPUR",
    "yf": "TARAPUR.NS"
  },
  {
    "name": "TARC Limited",
    "ticker": "TARC",
    "yf": "TARC.NS"
  },
  {
    "name": "Transformers And Rectifiers (India) Limited",
    "ticker": "TARIL",
    "yf": "TARIL.NS"
  },
  {
    "name": "Tarsons Products Limited",
    "ticker": "TARSONS",
    "yf": "TARSONS.NS"
  },
  {
    "name": "Tasty Bite Eatables Limited",
    "ticker": "TASTYBITE",
    "yf": "TASTYBITE.NS"
  },
  {
    "name": "Tata Capital Limited",
    "ticker": "TATACAP",
    "yf": "TATACAP.NS"
  },
  {
    "name": "Tata Chemicals Limited",
    "ticker": "TATACHEM",
    "yf": "TATACHEM.NS"
  },
  {
    "name": "Tata Communications Limited",
    "ticker": "TATACOMM",
    "yf": "TATACOMM.NS"
  },
  {
    "name": "TATA CONSUMER PRODUCTS LIMITED",
    "ticker": "TATACONSUM",
    "yf": "TATACONSUM.NS"
  },
  {
    "name": "Tata Elxsi Limited",
    "ticker": "TATAELXSI",
    "yf": "TATAELXSI.NS"
  },
  {
    "name": "Tata Investment Corporation Limited",
    "ticker": "TATAINVEST",
    "yf": "TATAINVEST.NS"
  },
  {
    "name": "Tata Power Company Limited",
    "ticker": "TATAPOWER",
    "yf": "TATAPOWER.NS"
  },
  {
    "name": "Tata Steel Limited",
    "ticker": "TATASTEEL",
    "yf": "TATASTEEL.NS"
  },
  {
    "name": "Tata Technologies Limited",
    "ticker": "TATATECH",
    "yf": "TATATECH.NS"
  },
  {
    "name": "Tatva Chintan Pharma Chem Limited",
    "ticker": "TATVA",
    "yf": "TATVA.NS"
  },
  {
    "name": "TBO Tek Limited",
    "ticker": "TBOTEK",
    "yf": "TBOTEK.NS"
  },
  {
    "name": "Tribhovandas Bhimji Zaveri Limited",
    "ticker": "TBZ",
    "yf": "TBZ.NS"
  },
  {
    "name": "TCC Concept Limited",
    "ticker": "TCC",
    "yf": "TCC.NS"
  },
  {
    "name": "Transport Corporation of India Limited",
    "ticker": "TCI",
    "yf": "TCI.NS"
  },
  {
    "name": "TCI Express Limited",
    "ticker": "TCIEXP",
    "yf": "TCIEXP.NS"
  },
  {
    "name": "TCI Finance Limited",
    "ticker": "TCIFINANCE",
    "yf": "TCIFINANCE.NS"
  },
  {
    "name": "TCPL Packaging Limited",
    "ticker": "TCPLPACK",
    "yf": "TCPLPACK.NS"
  },
  {
    "name": "Tata Consultancy Services Limited",
    "ticker": "TCS",
    "yf": "TCS.NS"
  },
  {
    "name": "TD Power Systems Limited",
    "ticker": "TDPOWERSYS",
    "yf": "TDPOWERSYS.NS"
  },
  {
    "name": "Team India Guaranty Limited",
    "ticker": "TEAMGTY",
    "yf": "TEAMGTY.NS"
  },
  {
    "name": "Teamlease Services Limited",
    "ticker": "TEAMLEASE",
    "yf": "TEAMLEASE.NS"
  },
  {
    "name": "Tech Mahindra Limited",
    "ticker": "TECHM",
    "yf": "TECHM.NS"
  },
  {
    "name": "Techno Electric & Engineering Company Limited",
    "ticker": "TECHNOE",
    "yf": "TECHNOE.NS"
  },
  {
    "name": "TechNVision Ventures Limited",
    "ticker": "TECHNVISN",
    "yf": "TECHNVISN.NS"
  },
  {
    "name": "TECIL Chemicals and Hydro Power Limited",
    "ticker": "TECILCHEM",
    "yf": "TECILCHEM.NS"
  },
  {
    "name": "Tega Industries Limited",
    "ticker": "TEGA",
    "yf": "TEGA.NS"
  },
  {
    "name": "Tejas Networks Limited",
    "ticker": "TEJASNET",
    "yf": "TEJASNET.NS"
  },
  {
    "name": "Tembo Global Industries Limited",
    "ticker": "TEMBO",
    "yf": "TEMBO.NS"
  },
  {
    "name": "Tenneco Clean Air India Limited",
    "ticker": "TENNIND",
    "yf": "TENNIND.NS"
  },
  {
    "name": "Tera Software Limited",
    "ticker": "TERASOFT",
    "yf": "TERASOFT.NS"
  },
  {
    "name": "Texmaco Infrastructure & Holdings Limited",
    "ticker": "TEXINFRA",
    "yf": "TEXINFRA.NS"
  },
  {
    "name": "Texmo Pipes and Products Limited",
    "ticker": "TEXMOPIPES",
    "yf": "TEXMOPIPES.NS"
  },
  {
    "name": "Texmaco Rail & Engineering Limited",
    "ticker": "TEXRAIL",
    "yf": "TEXRAIL.NS"
  },
  {
    "name": "Tourism Finance Corporation of India Limited",
    "ticker": "TFCILTD",
    "yf": "TFCILTD.NS"
  },
  {
    "name": "Transwarranty Finance Limited",
    "ticker": "TFL",
    "yf": "TFL.NS"
  },
  {
    "name": "TGB Banquets And Hotels Limited",
    "ticker": "TGBHOTELS",
    "yf": "TGBHOTELS.NS"
  },
  {
    "name": "Thacker & Company Limited",
    "ticker": "THACKER",
    "yf": "THACKER.NS"
  },
  {
    "name": "Thakkers Developers Limited",
    "ticker": "THAKDEV",
    "yf": "THAKDEV.NS"
  },
  {
    "name": "Thangamayil Jewellery Limited",
    "ticker": "THANGAMAYL",
    "yf": "THANGAMAYL.NS"
  },
  {
    "name": "The Investment Trust Of India Limited",
    "ticker": "THEINVEST",
    "yf": "THEINVEST.NS"
  },
  {
    "name": "Thejo Engineering Limited",
    "ticker": "THEJO",
    "yf": "THEJO.NS"
  },
  {
    "name": "Leela Palaces Hotels & Resorts Limited",
    "ticker": "THELEELA",
    "yf": "THELEELA.NS"
  },
  {
    "name": "Themis Medicare Limited",
    "ticker": "THEMISMED",
    "yf": "THEMISMED.NS"
  },
  {
    "name": "Thermax Limited",
    "ticker": "THERMAX",
    "yf": "THERMAX.NS"
  },
  {
    "name": "Thomas Cook  (India)  Limited",
    "ticker": "THOMASCOOK",
    "yf": "THOMASCOOK.NS"
  },
  {
    "name": "Thomas Scott (India) Limited",
    "ticker": "THOMASCOTT",
    "yf": "THOMASCOTT.NS"
  },
  {
    "name": "Thyrocare Technologies Limited",
    "ticker": "THYROCARE",
    "yf": "THYROCARE.NS"
  },
  {
    "name": "Tilaknagar Industries Limited",
    "ticker": "TI",
    "yf": "TI.NS"
  },
  {
    "name": "Twamev Construction and Infrastructure Limited",
    "ticker": "TICL",
    "yf": "TICL.NS"
  },
  {
    "name": "Tiger Logistics (India) Limited",
    "ticker": "TIGERLOGS",
    "yf": "TIGERLOGS.NS"
  },
  {
    "name": "Technocraft Industries (India) Limited",
    "ticker": "TIIL",
    "yf": "TIIL.NS"
  },
  {
    "name": "Tube Investments of India Limited",
    "ticker": "TIINDIA",
    "yf": "TIINDIA.NS"
  },
  {
    "name": "TIL Limited",
    "ticker": "TIL",
    "yf": "TIL.NS"
  },
  {
    "name": "Time Technoplast Limited",
    "ticker": "TIMETECHNO",
    "yf": "TIMETECHNO.NS"
  },
  {
    "name": "Timex Group India Limited",
    "ticker": "TIMEX",
    "yf": "TIMEX.NS"
  },
  {
    "name": "Timken India Limited",
    "ticker": "TIMKEN",
    "yf": "TIMKEN.NS"
  },
  {
    "name": "Tinna Rubber and Infrastructure Limited",
    "ticker": "TINNARUBR",
    "yf": "TINNARUBR.NS"
  },
  {
    "name": "Tips Films Limited",
    "ticker": "TIPSFILMS",
    "yf": "TIPSFILMS.NS"
  },
  {
    "name": "Tips Music Limited",
    "ticker": "TIPSMUSIC",
    "yf": "TIPSMUSIC.NS"
  },
  {
    "name": "Thirumalai Chemicals Limited",
    "ticker": "TIRUMALCHM",
    "yf": "TIRUMALCHM.NS"
  },
  {
    "name": "TITAGARH RAIL SYSTEMS LIMITED",
    "ticker": "TITAGARH",
    "yf": "TITAGARH.NS"
  },
  {
    "name": "Titan Company Limited",
    "ticker": "TITAN",
    "yf": "TITAN.NS"
  },
  {
    "name": "Tamilnad Mercantile Bank Limited",
    "ticker": "TMB",
    "yf": "TMB.NS"
  },
  {
    "name": "Tata Motors Limited",
    "ticker": "TMCV",
    "yf": "TMCV.NS"
  },
  {
    "name": "Tata Motors Passenger Vehicles Limited",
    "ticker": "TMPV",
    "yf": "TMPV.NS"
  },
  {
    "name": "Tamilnadu PetroProducts Limited",
    "ticker": "TNPETRO",
    "yf": "TNPETRO.NS"
  },
  {
    "name": "Tamil Nadu Newsprint & Papers Limited",
    "ticker": "TNPL",
    "yf": "TNPL.NS"
  },
  {
    "name": "Tamilnadu Telecommunication Limited",
    "ticker": "TNTELE",
    "yf": "TNTELE.NS"
  },
  {
    "name": "Tolins Tyres Limited",
    "ticker": "TOLINS",
    "yf": "TOLINS.NS"
  },
  {
    "name": "Torrent Pharmaceuticals Limited",
    "ticker": "TORNTPHARM",
    "yf": "TORNTPHARM.NS"
  },
  {
    "name": "Torrent Power Limited",
    "ticker": "TORNTPOWER",
    "yf": "TORNTPOWER.NS"
  },
  {
    "name": "Total Transport Systems Limited",
    "ticker": "TOTAL",
    "yf": "TOTAL.NS"
  },
  {
    "name": "Touchwood Entertainment Limited",
    "ticker": "TOUCHWOOD",
    "yf": "TOUCHWOOD.NS"
  },
  {
    "name": "Teamo Productions HQ Limited",
    "ticker": "TPHQ",
    "yf": "TPHQ.NS"
  },
  {
    "name": "TPL Plastech Limited",
    "ticker": "TPLPLASTEH",
    "yf": "TPLPLASTEH.NS"
  },
  {
    "name": "Tracxn Technologies Limited",
    "ticker": "TRACXN",
    "yf": "TRACXN.NS"
  },
  {
    "name": "Transpek Industry Limited",
    "ticker": "TRANSPEK",
    "yf": "TRANSPEK.NS"
  },
  {
    "name": "Transrail Lighting Limited",
    "ticker": "TRANSRAILL",
    "yf": "TRANSRAILL.NS"
  },
  {
    "name": "TRANSWORLD SHIPPING LINES LIMITED",
    "ticker": "TRANSWORLD",
    "yf": "TRANSWORLD.NS"
  },
  {
    "name": "Travel Food Services Limited",
    "ticker": "TRAVELFOOD",
    "yf": "TRAVELFOOD.NS"
  },
  {
    "name": "TREJHARA SOLUTIONS LIMITED",
    "ticker": "TREJHARA",
    "yf": "TREJHARA.NS"
  },
  {
    "name": "Transindia Real Estate Limited",
    "ticker": "TREL",
    "yf": "TREL.NS"
  },
  {
    "name": "Trent Limited",
    "ticker": "TRENT",
    "yf": "TRENT.NS"
  },
  {
    "name": "TRF Limited",
    "ticker": "TRF",
    "yf": "TRF.NS"
  },
  {
    "name": "Trident Limited",
    "ticker": "TRIDENT",
    "yf": "TRIDENT.NS"
  },
  {
    "name": "Trigyn Technologies Limited",
    "ticker": "TRIGYN",
    "yf": "TRIGYN.NS"
  },
  {
    "name": "Triveni Turbine Limited",
    "ticker": "TRITURBINE",
    "yf": "TRITURBINE.NS"
  },
  {
    "name": "Triveni Engineering & Industries Limited",
    "ticker": "TRIVENI",
    "yf": "TRIVENI.NS"
  },
  {
    "name": "TruCap Finance Limited",
    "ticker": "TRU",
    "yf": "TRU.NS"
  },
  {
    "name": "TruAlt Bioenergy Limited",
    "ticker": "TRUALT",
    "yf": "TRUALT.NS"
  },
  {
    "name": "TSF INVESTMENTS LIMITED",
    "ticker": "TSFINV",
    "yf": "TSFINV.NS"
  },
  {
    "name": "TTK Healthcare Limited",
    "ticker": "TTKHLTCARE",
    "yf": "TTKHLTCARE.NS"
  },
  {
    "name": "TTK Prestige Limited",
    "ticker": "TTKPRESTIG",
    "yf": "TTKPRESTIG.NS"
  },
  {
    "name": "Tata Teleservices (Maharashtra) Limited",
    "ticker": "TTML",
    "yf": "TTML.NS"
  },
  {
    "name": "TVS Electronics Limited",
    "ticker": "TVSELECT",
    "yf": "TVSELECT.NS"
  },
  {
    "name": "TVS Holdings Limited",
    "ticker": "TVSHLTD",
    "yf": "TVSHLTD.NS"
  },
  {
    "name": "TVS Motor Company Limited",
    "ticker": "TVSMOTOR",
    "yf": "TVSMOTOR.NS"
  },
  {
    "name": "TVS Srichakra Limited",
    "ticker": "TVSSRICHAK",
    "yf": "TVSSRICHAK.NS"
  },
  {
    "name": "TV Today Network Limited",
    "ticker": "TVTODAY",
    "yf": "TVTODAY.NS"
  },
  {
    "name": "TV Vision Limited",
    "ticker": "TVVISION",
    "yf": "TVVISION.NS"
  },
  {
    "name": "United Breweries Limited",
    "ticker": "UBL",
    "yf": "UBL.NS"
  },
  {
    "name": "UCAL LIMITED",
    "ticker": "UCAL",
    "yf": "UCAL.NS"
  },
  {
    "name": "UCO Bank",
    "ticker": "UCOBANK",
    "yf": "UCOBANK.NS"
  },
  {
    "name": "Updater Services Limited",
    "ticker": "UDS",
    "yf": "UDS.NS"
  },
  {
    "name": "Ujaas Energy Limited",
    "ticker": "UEL",
    "yf": "UEL.NS"
  },
  {
    "name": "United Foodbrands Limited",
    "ticker": "UFBL",
    "yf": "UFBL.NS"
  },
  {
    "name": "UFLEX Limited",
    "ticker": "UFLEX",
    "yf": "UFLEX.NS"
  },
  {
    "name": "UFO Moviez India Limited",
    "ticker": "UFO",
    "yf": "UFO.NS"
  },
  {
    "name": "The Ugar Sugar Works Limited",
    "ticker": "UGARSUGAR",
    "yf": "UGARSUGAR.NS"
  },
  {
    "name": "Ugro Capital Limited",
    "ticker": "UGROCAP",
    "yf": "UGROCAP.NS"
  },
  {
    "name": "Ujjivan Small Finance Bank Limited",
    "ticker": "UJJIVANSFB",
    "yf": "UJJIVANSFB.NS"
  },
  {
    "name": "UltraTech Cement Limited",
    "ticker": "ULTRACEMCO",
    "yf": "ULTRACEMCO.NS"
  },
  {
    "name": "Ultramarine & Pigments Limited",
    "ticker": "ULTRAMAR",
    "yf": "ULTRAMAR.NS"
  },
  {
    "name": "UMIYA BUILDCON LIMITED",
    "ticker": "UMIYA-MRO",
    "yf": "UMIYA-MRO.NS"
  },
  {
    "name": "Unichem Laboratories Limited",
    "ticker": "UNICHEMLAB",
    "yf": "UNICHEMLAB.NS"
  },
  {
    "name": "United Drilling Tools Limited",
    "ticker": "UNIDT",
    "yf": "UNIDT.NS"
  },
  {
    "name": "Unicommerce Esolutions Limited",
    "ticker": "UNIECOM",
    "yf": "UNIECOM.NS"
  },
  {
    "name": "Uniphos Enterprises Limited",
    "ticker": "UNIENTER",
    "yf": "UNIENTER.NS"
  },
  {
    "name": "Unimech Aerospace and Manufacturing Limited",
    "ticker": "UNIMECH",
    "yf": "UNIMECH.NS"
  },
  {
    "name": "Union Bank of India",
    "ticker": "UNIONBANK",
    "yf": "UNIONBANK.NS"
  },
  {
    "name": "Uniparts India Limited",
    "ticker": "UNIPARTS",
    "yf": "UNIPARTS.NS"
  },
  {
    "name": "United Spirits Limited",
    "ticker": "UNITDSPR",
    "yf": "UNITDSPR.NS"
  },
  {
    "name": "Unitech Limited",
    "ticker": "UNITECH",
    "yf": "UNITECH.NS"
  },
  {
    "name": "United Polyfab Gujarat Limited",
    "ticker": "UNITEDPOLY",
    "yf": "UNITEDPOLY.NS"
  },
  {
    "name": "The United Nilgiri Tea Estates Company Limited",
    "ticker": "UNITEDTEA",
    "yf": "UNITEDTEA.NS"
  },
  {
    "name": "Univastu India Limited",
    "ticker": "UNIVASTU",
    "yf": "UNIVASTU.NS"
  },
  {
    "name": "Universal Cables Limited",
    "ticker": "UNIVCABLES",
    "yf": "UNIVCABLES.NS"
  },
  {
    "name": "UNO Minda Limited",
    "ticker": "UNOMINDA",
    "yf": "UNOMINDA.NS"
  },
  {
    "name": "UPL Limited",
    "ticker": "UPL",
    "yf": "UPL.NS"
  },
  {
    "name": "Urban Company Limited",
    "ticker": "URBANCO",
    "yf": "URBANCO.NS"
  },
  {
    "name": "Urja Global Limited",
    "ticker": "URJA",
    "yf": "URJA.NS"
  },
  {
    "name": "Usha Martin Limited",
    "ticker": "USHAMART",
    "yf": "USHAMART.NS"
  },
  {
    "name": "UTI Asset Management Company Limited",
    "ticker": "UTIAMC",
    "yf": "UTIAMC.NS"
  },
  {
    "name": "Utkarsh Small Finance Bank Limited",
    "ticker": "UTKARSHBNK",
    "yf": "UTKARSHBNK.NS"
  },
  {
    "name": "Fujiyama Power Systems Limited",
    "ticker": "UTLSOLAR",
    "yf": "UTLSOLAR.NS"
  },
  {
    "name": "Uttam Sugar Mills Limited",
    "ticker": "UTTAMSUGAR",
    "yf": "UTTAMSUGAR.NS"
  },
  {
    "name": "U. Y. Fincorp Limited",
    "ticker": "UYFINCORP",
    "yf": "UYFINCORP.NS"
  },
  {
    "name": "V2 Retail Limited",
    "ticker": "V2RETAIL",
    "yf": "V2RETAIL.NS"
  },
  {
    "name": "Vadilal Industries Limited",
    "ticker": "VADILALIND",
    "yf": "VADILALIND.NS"
  },
  {
    "name": "Vaibhav Global Limited",
    "ticker": "VAIBHAVGBL",
    "yf": "VAIBHAVGBL.NS"
  },
  {
    "name": "Vakrangee Limited",
    "ticker": "VAKRANGEE",
    "yf": "VAKRANGEE.NS"
  },
  {
    "name": "Valiant Organics Limited",
    "ticker": "VALIANTORG",
    "yf": "VALIANTORG.NS"
  },
  {
    "name": "Vardhman Acrylics Limited",
    "ticker": "VARDHACRLC",
    "yf": "VARDHACRLC.NS"
  },
  {
    "name": "Varroc Engineering Limited",
    "ticker": "VARROC",
    "yf": "VARROC.NS"
  },
  {
    "name": "Vascon Engineers Limited",
    "ticker": "VASCONEQ",
    "yf": "VASCONEQ.NS"
  },
  {
    "name": "Vaswani Industries Limited",
    "ticker": "VASWANI",
    "yf": "VASWANI.NS"
  },
  {
    "name": "Varun Beverages Limited",
    "ticker": "VBL",
    "yf": "VBL.NS"
  },
  {
    "name": "Vaxtex Cotfab Limited",
    "ticker": "VCL",
    "yf": "VCL.NS"
  },
  {
    "name": "Vedanta Limited",
    "ticker": "VEDL",
    "yf": "VEDL.NS"
  },
  {
    "name": "Veedol Corporation Limited",
    "ticker": "VEEDOL",
    "yf": "VEEDOL.NS"
  },
  {
    "name": "Veljan Denison Limited",
    "ticker": "VELJAN",
    "yf": "VELJAN.NS"
  },
  {
    "name": "Venky's (India) Limited",
    "ticker": "VENKEYS",
    "yf": "VENKEYS.NS"
  },
  {
    "name": "Ventive Hospitality Limited",
    "ticker": "VENTIVE",
    "yf": "VENTIVE.NS"
  },
  {
    "name": "Venus Pipes & Tubes Limited",
    "ticker": "VENUSPIPES",
    "yf": "VENUSPIPES.NS"
  },
  {
    "name": "Venus Remedies Limited",
    "ticker": "VENUSREM",
    "yf": "VENUSREM.NS"
  },
  {
    "name": "Veranda Learning Solutions Limited",
    "ticker": "VERANDA",
    "yf": "VERANDA.NS"
  },
  {
    "name": "Vertoz Limited",
    "ticker": "VERTOZ",
    "yf": "VERTOZ.NS"
  },
  {
    "name": "Vesuvius India Limited",
    "ticker": "VESUVIUS",
    "yf": "VESUVIUS.NS"
  },
  {
    "name": "Veto Switchgears And Cables Limited",
    "ticker": "VETO",
    "yf": "VETO.NS"
  },
  {
    "name": "VARVEE GLOBAL LIMITED",
    "ticker": "VGL",
    "yf": "VGL.NS"
  },
  {
    "name": "V-Guard Industries Limited",
    "ticker": "VGUARD",
    "yf": "VGUARD.NS"
  },
  {
    "name": "Vardhman Holdings Limited",
    "ticker": "VHL",
    "yf": "VHL.NS"
  },
  {
    "name": "Vidhi Specialty Food Ingredients Limited",
    "ticker": "VIDHIING",
    "yf": "VIDHIING.NS"
  },
  {
    "name": "Vidya Wires Limited",
    "ticker": "VIDYAWIRES",
    "yf": "VIDYAWIRES.NS"
  },
  {
    "name": "Vijaya Diagnostic Centre Limited",
    "ticker": "VIJAYA",
    "yf": "VIJAYA.NS"
  },
  {
    "name": "Vikram Solar Limited",
    "ticker": "VIKRAMSOLR",
    "yf": "VIKRAMSOLR.NS"
  },
  {
    "name": "Vikran Engineering Limited",
    "ticker": "VIKRAN",
    "yf": "VIKRAN.NS"
  },
  {
    "name": "Vimta Labs Limited",
    "ticker": "VIMTALABS",
    "yf": "VIMTALABS.NS"
  },
  {
    "name": "Vinati Organics Limited",
    "ticker": "VINATIORGA",
    "yf": "VINATIORGA.NS"
  },
  {
    "name": "Vintage Coffee And Beverages Limited",
    "ticker": "VINCOFE",
    "yf": "VINCOFE.NS"
  },
  {
    "name": "Vindhya Telelinks Limited",
    "ticker": "VINDHYATEL",
    "yf": "VINDHYATEL.NS"
  },
  {
    "name": "Vinny Overseas Limited",
    "ticker": "VINNY",
    "yf": "VINNY.NS"
  },
  {
    "name": "Vinyl Chemicals (India) Limited",
    "ticker": "VINYLINDIA",
    "yf": "VINYLINDIA.NS"
  },
  {
    "name": "VIP Clothing Limited",
    "ticker": "VIPCLOTHNG",
    "yf": "VIPCLOTHNG.NS"
  },
  {
    "name": "VIP Industries Limited",
    "ticker": "VIPIND",
    "yf": "VIPIND.NS"
  },
  {
    "name": "Visaka Industries Limited",
    "ticker": "VISAKAIND",
    "yf": "VISAKAIND.NS"
  },
  {
    "name": "Visa Steel Limited",
    "ticker": "VISASTEEL",
    "yf": "VISASTEEL.NS"
  },
  {
    "name": "Vishnu Chemicals Limited",
    "ticker": "VISHNU",
    "yf": "VISHNU.NS"
  },
  {
    "name": "Visagar Polytex Limited",
    "ticker": "VIVIDHA",
    "yf": "VIVIDHA.NS"
  },
  {
    "name": "Viyash Scientific Limited",
    "ticker": "VIYASH",
    "yf": "VIYASH.NS"
  },
  {
    "name": "VLS Finance Limited",
    "ticker": "VLSFINANCE",
    "yf": "VLSFINANCE.NS"
  },
  {
    "name": "V-Mart Retail Limited",
    "ticker": "VMART",
    "yf": "VMART.NS"
  },
  {
    "name": "Vishal Mega Mart Limited",
    "ticker": "VMM",
    "yf": "VMM.NS"
  },
  {
    "name": "VMS TMT Limited",
    "ticker": "VMSTMT",
    "yf": "VMSTMT.NS"
  },
  {
    "name": "Voltamp Transformers Limited",
    "ticker": "VOLTAMP",
    "yf": "VOLTAMP.NS"
  },
  {
    "name": "Voltas Limited",
    "ticker": "VOLTAS",
    "yf": "VOLTAS.NS"
  },
  {
    "name": "Vishnu Prakash R Punglia Limited",
    "ticker": "VPRPL",
    "yf": "VPRPL.NS"
  },
  {
    "name": "Vraj Iron and Steel Limited",
    "ticker": "VRAJ",
    "yf": "VRAJ.NS"
  },
  {
    "name": "VRL Logistics Limited",
    "ticker": "VRLLOG",
    "yf": "VRLLOG.NS"
  },
  {
    "name": "Vardhman Special Steels Limited",
    "ticker": "VSSL",
    "yf": "VSSL.NS"
  },
  {
    "name": "VST Industries Limited",
    "ticker": "VSTIND",
    "yf": "VSTIND.NS"
  },
  {
    "name": "Vibhor Steel Tubes Limited",
    "ticker": "VSTL",
    "yf": "VSTL.NS"
  },
  {
    "name": "V.S.T Tillers Tractors Limited",
    "ticker": "VSTTILLERS",
    "yf": "VSTTILLERS.NS"
  },
  {
    "name": "Vardhman Textiles Limited",
    "ticker": "VTL",
    "yf": "VTL.NS"
  },
  {
    "name": "Waaree Energies Limited",
    "ticker": "WAAREEENER",
    "yf": "WAAREEENER.NS"
  },
  {
    "name": "Waaree Renewable Technologies Limited",
    "ticker": "WAAREERTL",
    "yf": "WAAREERTL.NS"
  },
  {
    "name": "VA Tech Wabag Limited",
    "ticker": "WABAG",
    "yf": "WABAG.NS"
  },
  {
    "name": "Wakefit Innovations Limited",
    "ticker": "WAKEFIT",
    "yf": "WAKEFIT.NS"
  },
  {
    "name": "Walchandnagar Industries Limited",
    "ticker": "WALCHANNAG",
    "yf": "WALCHANNAG.NS"
  },
  {
    "name": "Western Carriers (India) Limited",
    "ticker": "WCIL",
    "yf": "WCIL.NS"
  },
  {
    "name": "Wealth First Portfolio Managers Limited",
    "ticker": "WEALTH",
    "yf": "WEALTH.NS"
  },
  {
    "name": "Websol Energy System Limited",
    "ticker": "WEBELSOLAR",
    "yf": "WEBELSOLAR.NS"
  },
  {
    "name": "Weizmann Limited",
    "ticker": "WEIZMANIND",
    "yf": "WEIZMANIND.NS"
  },
  {
    "name": "Wonder Electricals Limited",
    "ticker": "WEL",
    "yf": "WEL.NS"
  },
  {
    "name": "Welspun Corp Limited",
    "ticker": "WELCORP",
    "yf": "WELCORP.NS"
  },
  {
    "name": "Welspun Enterprises Limited",
    "ticker": "WELENT",
    "yf": "WELENT.NS"
  },
  {
    "name": "Welspun Investments and Commercials Limited",
    "ticker": "WELINV",
    "yf": "WELINV.NS"
  },
  {
    "name": "Welspun Specialty Solutions Limited",
    "ticker": "WELSPLSOL",
    "yf": "WELSPLSOL.NS"
  },
  {
    "name": "Welspun Living Limited",
    "ticker": "WELSPUNLIV",
    "yf": "WELSPUNLIV.NS"
  },
  {
    "name": "Wendt (India) Limited",
    "ticker": "WENDT",
    "yf": "WENDT.NS"
  },
  {
    "name": "WESTLIFE FOODWORLD LIMITED",
    "ticker": "WESTLIFE",
    "yf": "WESTLIFE.NS"
  },
  {
    "name": "WE WIN LIMITED",
    "ticker": "WEWIN",
    "yf": "WEWIN.NS"
  },
  {
    "name": "WeWork India Management Limited",
    "ticker": "WEWORK",
    "yf": "WEWORK.NS"
  },
  {
    "name": "Wheels India Limited",
    "ticker": "WHEELS",
    "yf": "WHEELS.NS"
  },
  {
    "name": "Whirlpool of India Limited",
    "ticker": "WHIRLPOOL",
    "yf": "WHIRLPOOL.NS"
  },
  {
    "name": "Williamson Magor & Company Limited",
    "ticker": "WILLAMAGOR",
    "yf": "WILLAMAGOR.NS"
  },
  {
    "name": "Wim Plast Limited",
    "ticker": "WIMPLAST",
    "yf": "WIMPLAST.NS"
  },
  {
    "name": "Windlas Biotech Limited",
    "ticker": "WINDLAS",
    "yf": "WINDLAS.NS"
  },
  {
    "name": "Windsor Machines Limited",
    "ticker": "WINDMACHIN",
    "yf": "WINDMACHIN.NS"
  },
  {
    "name": "The Western India Plywoods Limited",
    "ticker": "WIPL",
    "yf": "WIPL.NS"
  },
  {
    "name": "Wipro Limited",
    "ticker": "WIPRO",
    "yf": "WIPRO.NS"
  },
  {
    "name": "Wockhardt Limited",
    "ticker": "WOCKPHARMA",
    "yf": "WOCKPHARMA.NS"
  },
  {
    "name": "Wonderla Holidays Limited",
    "ticker": "WONDERLA",
    "yf": "WONDERLA.NS"
  },
  {
    "name": "Worth Peripherals Limited",
    "ticker": "WORTHPERI",
    "yf": "WORTHPERI.NS"
  },
  {
    "name": "WPIL Limited",
    "ticker": "WPIL",
    "yf": "WPIL.NS"
  },
  {
    "name": "W S Industries (I) Limited",
    "ticker": "WSI",
    "yf": "WSI.NS"
  },
  {
    "name": "West Coast Paper Mills Limited",
    "ticker": "WSTCSTPAPR",
    "yf": "WSTCSTPAPR.NS"
  },
  {
    "name": "Xchanging Solutions Limited",
    "ticker": "XCHANGING",
    "yf": "XCHANGING.NS"
  },
  {
    "name": "Xelpmoc Design And Tech Limited",
    "ticker": "XELPMOC",
    "yf": "XELPMOC.NS"
  },
  {
    "name": "Xpro India Limited",
    "ticker": "XPROINDIA",
    "yf": "XPROINDIA.NS"
  },
  {
    "name": "Xtglobal Infotech Limited",
    "ticker": "XTGLOBAL",
    "yf": "XTGLOBAL.NS"
  },
  {
    "name": "Yasho Industries Limited",
    "ticker": "YASHO",
    "yf": "YASHO.NS"
  },
  {
    "name": "Yatharth Hospital & Trauma Care Services Limited",
    "ticker": "YATHARTH",
    "yf": "YATHARTH.NS"
  },
  {
    "name": "Yatra Online Limited",
    "ticker": "YATRA",
    "yf": "YATRA.NS"
  },
  {
    "name": "Yes Bank Limited",
    "ticker": "YESBANK",
    "yf": "YESBANK.NS"
  },
  {
    "name": "Yuken India Limited",
    "ticker": "YUKEN",
    "yf": "YUKEN.NS"
  },
  {
    "name": "Zaggle Prepaid Ocean Services Limited",
    "ticker": "ZAGGLE",
    "yf": "ZAGGLE.NS"
  },
  {
    "name": "Zee Entertainment Enterprises Limited",
    "ticker": "ZEEL",
    "yf": "ZEEL.NS"
  },
  {
    "name": "Zee Learn Limited",
    "ticker": "ZEELEARN",
    "yf": "ZEELEARN.NS"
  },
  {
    "name": "Zenith Exports Limited",
    "ticker": "ZENITHEXPO",
    "yf": "ZENITHEXPO.NS"
  },
  {
    "name": "Zenith Steel Pipes & Industries Limited",
    "ticker": "ZENITHSTL",
    "yf": "ZENITHSTL.NS"
  },
  {
    "name": "Zensar Technologies Limited",
    "ticker": "ZENSARTECH",
    "yf": "ZENSARTECH.NS"
  },
  {
    "name": "Zen Technologies Limited",
    "ticker": "ZENTEC",
    "yf": "ZENTEC.NS"
  },
  {
    "name": "ZF Commercial Vehicle Control Systems India Limited",
    "ticker": "ZFCVINDIA",
    "yf": "ZFCVINDIA.NS"
  },
  {
    "name": "ZF Steering Gear (India) Limited",
    "ticker": "ZFSTEERING",
    "yf": "ZFSTEERING.NS"
  },
  {
    "name": "Zim Laboratories Limited",
    "ticker": "ZIMLAB",
    "yf": "ZIMLAB.NS"
  },
  {
    "name": "Zodiac Clothing Company Limited",
    "ticker": "ZODIACLOTH",
    "yf": "ZODIACLOTH.NS"
  },
  {
    "name": "Zota Health Care LImited",
    "ticker": "ZOTA",
    "yf": "ZOTA.NS"
  },
  {
    "name": "Saraswati Commercial India Limited",
    "ticker": "ZSARACOM",
    "yf": "ZSARACOM.NS"
  },
  {
    "name": "Zuari Agro Chemicals Limited",
    "ticker": "ZUARI",
    "yf": "ZUARI.NS"
  },
  {
    "name": "ZUARI INDUSTRIES LIMITED",
    "ticker": "ZUARIIND",
    "yf": "ZUARIIND.NS"
  },
  {
    "name": "Zydus Lifesciences Limited",
    "ticker": "ZYDUSLIFE",
    "yf": "ZYDUSLIFE.NS"
  },
  {
    "name": "Zydus Wellness Limited",
    "ticker": "ZYDUSWELL",
    "yf": "ZYDUSWELL.NS"
  }
]

def collect_financials(company):
    try:
        stock = yf.Ticker(company["yf"])
        info = stock.info
        data = {
            "ticker":        company["ticker"],
            "collected_at":  datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "company_info": {
                "name":           info.get("longName", company["name"]),
                "sector":         info.get("sector", "N/A"),
                "industry":       info.get("industry", "N/A"),
                "market_cap":     info.get("marketCap", "N/A"),
                "current_price":  info.get("currentPrice", "N/A"),
                "pe_ratio":       info.get("trailingPE", "N/A"),
                "pb_ratio":       info.get("priceToBook", "N/A"),
                "roe":            info.get("returnOnEquity", "N/A"),
                "debt_to_equity": info.get("debtToEquity", "N/A"),
                "revenue":        info.get("totalRevenue", "N/A"),
                "net_income":     info.get("netIncomeToCommon", "N/A"),
                "eps":            info.get("trailingEps", "N/A"),
                "52_week_high":   info.get("fiftyTwoWeekHigh", "N/A"),
                "52_week_low":    info.get("fiftyTwoWeekLow", "N/A"),
                "dividend_yield": info.get("dividendYield", "N/A"),
            }
        }
        with open(f"data/financials/{company['ticker']}.json", "w") as f:
            json.dump(data, f, indent=2, default=str)
        print(f"  Saved {company['ticker']}")
    except Exception as e:
        print(f"  Failed {company['ticker']}: {e}")

def collect_news(company):
    try:
        query = company["name"].replace(" ", "+") + "+NSE+stock"
        url = f"https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        root = ET.fromstring(response.content)
        articles = []
        for item in root.findall(".//item")[:10]:
            articles.append({
                "title":     item.findtext("title", "N/A"),
                "link":      item.findtext("link", "N/A"),
                "published": item.findtext("pubDate", "N/A"),
                "source":    item.findtext("source", "N/A"),
            })
        data = {
            "company":      company["name"],
            "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "articles":     articles
        }
        with open(f"data/news/{company['ticker']}_news.json", "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"  Failed news {company['ticker']}: {e}")


def collect_directors(company):
    try:
        stock = yf.Ticker(company["yf"])
        info = stock.info
        officers = info.get("companyOfficers", [])
        directors = []
        for o in officers:
            pay = o.get("totalPay", "N/A")
            if isinstance(pay, dict):
                pay = pay.get("raw", "N/A")
            directors.append({
                "name":      o.get("name", "N/A"),
                "role":      o.get("title", "N/A"),
                "age":       o.get("age", "N/A"),
                "year_born": o.get("yearBorn", "N/A"),
                "total_pay": pay,
            })
        data = {
            "ticker":       company["ticker"],
            "company":      company["name"],
            "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "directors":    directors
        }
        os.makedirs("data/directors", exist_ok=True)
        with open(f"data/directors/{company['ticker']}_directors.json", "w") as f:
            json.dump(data, f, indent=2, default=str)
        print(f"  Directors saved {company['ticker']} ({len(directors)} found)")
    except Exception as e:
        print(f"  Failed directors {company['ticker']}: {e}")

print(f"Starting data collection for {len(COMPANIES)} companies...")
for i, company in enumerate(COMPANIES, 1):
    print(f"[{i}/{len(COMPANIES)}] {company['ticker']}")
    collect_financials(company)
    collect_news(company)
    collect_directors(company)
    time.sleep(0.5)

print("\nAll done!")

import sys, os, subprocess, time, asyncio
from playwright.async_api import async_playwright
SITE=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','site')
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','shots')
os.makedirs(OUT,exist_ok=True)
pages=sys.argv[1:] or ['index.html']
async def main():
    srv=subprocess.Popen([sys.executable,'-m','http.server','8765','--bind','127.0.0.1'],cwd=SITE,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    time.sleep(1)
    try:
        async with async_playwright() as p:
            b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
            for name,w,h in (('d',1440,900),('m',390,844)):
                ctx=await b.new_context(viewport={'width':w,'height':h},device_scale_factor=1)
                await ctx.add_init_script("try{localStorage.setItem('regius-age','yes')}catch(e){}")
                pg=await ctx.new_page()
                errs=[]
                pg.on('console',lambda m: errs.append(m.text) if m.type=='error' else None)
                pg.on('pageerror',lambda e: errs.append(str(e)))
                for page in pages:
                    gate = page.endswith('?gate')
                    url='http://127.0.0.1:8765/'+page.replace('?gate','')
                    if gate:
                        c2=await b.new_context(viewport={'width':w,'height':h}); pg2=await c2.new_page()
                        await pg2.goto(url); await pg2.wait_for_timeout(900)
                        await pg2.screenshot(path=os.path.join(OUT,f"gate-{name}.png")); await c2.close(); continue
                    await pg.goto(url); await pg.wait_for_timeout(1500)
                    await pg.screenshot(path=os.path.join(OUT,f"{page[:-5]}-{name}.png"),full_page=True)
                    ov=await pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
                    print(page,name,'overflow-x',ov,'errors',errs[:3])
                await ctx.close()
            await b.close()
    finally:
        srv.terminate()
asyncio.run(main())

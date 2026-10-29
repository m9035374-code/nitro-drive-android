from pathlib import Path
from datetime import datetime
import shutil
import sys

game = Path("index.html")
if not game.exists():
    sys.exit("❌ مش لاقي index.html. اتأكد إنك داخل ~/lab/nitro-dev")

html = game.read_text(encoding="utf-8")

marker = "/* NITRO_SPEED_STREAKS_V1 */"
if marker in html:
    sys.exit("ℹ️ تأثير السرعة موجود بالفعل، مفيش تعديل اتعمل.")

draw_anchor = """function draw(){
  drawRoad();
  enemies.forEach(e=>drawCar(e.x,e.y,e.color));
  drawCar(player.x,player.y,playerColor,true);
}"""

if draw_anchor not in html:
    sys.exit("❌ شكل دالة draw مختلف. مفيش تعديل اتعمل حفاظًا على اللعبة.")

effect = """/* NITRO_SPEED_STREAKS_V1 */
function drawSpeedStreaks(){
  const boost = nitroFrames > 0;
  const intensity = Math.max(0, Math.min(1, (speed - 80) / 140));
  if(intensity < 0.04 && !boost) return;

  ctx.save();
  ctx.lineCap = 'round';

  for(let i=0; i<15; i++){
    const x = 82 + ((i * 47) % 226);
    const drift = (i % 3) * 19;
    const travel = roadOffset * (1.2 + (i % 4) * 0.22);
    const y = ((i * 89 + drift + travel) % 650) - 25;
    const length = 9 + intensity * 27 + (boost ? 15 : 0);
    const alpha = 0.12 + intensity * 0.28 + (boost ? 0.18 : 0);

    ctx.globalAlpha = Math.min(alpha, 0.62);
    ctx.strokeStyle = boost ? '#8df7ff' : '#d8e9f5';
    ctx.lineWidth = boost ? 2 : 1.2;
    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.lineTo(x, y + length);
    ctx.stroke();
  }

  if(boost){
    ctx.globalAlpha = 0.12;
    ctx.fillStyle = '#19dfff';
    ctx.fillRect(74, 0, 5, 600);
    ctx.fillRect(311, 0, 5, 600);
  }

  ctx.restore();
}

"""

new_draw = """function draw(){
  drawRoad();
  drawSpeedStreaks();
  enemies.forEach(e=>drawCar(e.x,e.y,e.color));
  drawCar(player.x,player.y,playerColor,true);
}"""

backup = Path("backup-speed-effects-" +
              datetime.now().strftime("%Y%m%d-%H%M%S") + ".html")

shutil.copy2(game, backup)
html = html.replace(draw_anchor, effect + new_draw, 1)
game.write_text(html, encoding="utf-8")

print("✅ تمت إضافة تأثير خطوط السرعة!")
print("🛡️ النسخة الاحتياطية:", backup)
print("🏁 الملف المعدل:", game)

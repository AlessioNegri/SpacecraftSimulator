/**
 * Paint a space capsule.
 * 
 * @AlessioNegri
 * 
 * @param {2D Canvas Context} ctx 
 * @param {Canvas Width} width 
 * @param {Canvas Height} height 
 */
function paint(ctx, width, height)
{
    let d = 50

    // --- CAPSULE 

    // * Draw heat shield

    pen(ctx, "#FFFFFF", "#80FF8000", 3, "")

    ctx.beginPath()
    ctx.moveTo(d, height / 2)
    ctx.bezierCurveTo(d, d + height / 2, width - d, d + height / 2, width - d, height / 2)
    ctx.closePath()
    ctx.stroke()
    ctx.fill()

    // * Draw cone

    pen(ctx, "#FFFFFF", "#40FFFFFF", 3, "")

    ctx.beginPath()
    ctx.moveTo(d, height / 2)
    ctx.lineTo(width - d, height / 2)
    ctx.lineTo(width / 2 + d / 2, height / 2 - width / 2)
    ctx.lineTo(width / 2 - d / 2, height / 2 - width / 2)
    ctx.closePath()
    ctx.stroke()
    ctx.fill()

    // --- GEOMETRY 

    // * Axis

    pen(ctx, "#FFFFFF", "#FFFFFF", 1, "")

    ctx.beginPath()
    ctx.setLineDash([5, 15])
    ctx.moveTo(width / 2, 0)
    ctx.lineTo(width / 2, height)
    ctx.stroke()

    // * Projections

    ctx.beginPath()
    ctx.moveTo(d, height / 2)
    ctx.lineTo(d, height / 2 - 200)
    ctx.stroke()

    ctx.beginPath()
    ctx.moveTo(250, height / 2)
    ctx.lineTo(width / 2, height / 2 - 300)
    ctx.stroke()

    ctx.beginPath()
    ctx.setLineDash([])
    ctx.moveTo(width / 2, height / 2 - 300)
    ctx.lineTo(75, height / 2 + 25)
    ctx.stroke()

    ctx.beginPath()
    ctx.moveTo(width / 2, height / 2 - 25)
    ctx.lineTo(width / 2 + width / 3, height / 2 - 25)
    ctx.stroke()

    // * Arcs

    pen(ctx, "#FFFFFF", "#FFFFFF", 1, "")

    ctx.beginPath()
    ctx.moveTo(d, height / 2)
    ctx.arc(d, height / 2, 75, -Math.PI / 3 - 0.05, -Math.PI / 2, true)
    ctx.lineTo(d, height / 2)
    ctx.stroke()

    ctx.beginPath()
    ctx.moveTo(width / 2, height / 2 - 300)
    ctx.arc(width / 2, height / 2 - 300, 75, Math.PI / 2.525, Math.PI / 2, false)
    ctx.lineTo(width / 2, height / 2 - 300)
    ctx.stroke()

    // * Labels

    pen(ctx, "#FFFFFF", "#FFFFFF", 1, "20px sans-serif")

    ctx.fillText("φ_C", d + 10, height / 2 - 100)
    ctx.fillText("φ_1", width / 2 + d, height / 2 - 200)
    ctx.fillText("R_N", width / 2 - 1.5 * d, height / 2 - 200)
    ctx.fillText("R_B", width / 2 + 10, height / 2 - 50)

    // --- SHOCK WAVE 

    // * Draw heat shield

    pen(ctx, "#FF9000", "#FFFFFF", 3, "")

    let dist = 25

    ctx.beginPath()
    ctx.moveTo(25, height / 2 + dist)
    ctx.bezierCurveTo(25, 50 + height / 2 + dist, 275, 50 + height / 2 + dist, 275, height / 2 + dist)
    ctx.stroke()

    // * Text

    ctx.font        = "25px sans-serif"
    ctx.fillStyle   = Qt.rgba(255, 255, 255, 1)

    ctx.fillText("SHOCK WAVE", width / 2 - 75, 50 + height / 2 + dist + 25)
}

function pen(ctx, strokeStyle, fillStyle, lineWidth, font)
{
    ctx.strokeStyle = strokeStyle
    ctx.fillStyle   = fillStyle
    ctx.lineWidth   = lineWidth
    ctx.font        = (font === "") ? "12px sans-serif" : font
}
var LZString = {
    _keyStr: "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",
    _f: String.fromCharCode,
    compressToBase64: function(c) {
        if (c == null) {
            return ""
        }
        var a = "";
        var k, h, f, j, g, e, d;
        var b = 0;
        c = LZString.compress(c);
        while (b < c.length * 2) {
            if (b % 2 == 0) {
                k = c.charCodeAt(b / 2) >> 8;
                h = c.charCodeAt(b / 2) & 255;
                if (b / 2 + 1 < c.length) {
                    f = c.charCodeAt(b / 2 + 1) >> 8
                } else {
                    f = NaN
                }
            } else {
                k = c.charCodeAt((b - 1) / 2) & 255;
                if ((b + 1) / 2 < c.length) {
                    h = c.charCodeAt((b + 1) / 2) >> 8;
                    f = c.charCodeAt((b + 1) / 2) & 255
                } else {
                    h = f = NaN
                }
            }
            b += 3;
            j = k >> 2;
            g = ((k & 3) << 4) | (h >> 4);
            e = ((h & 15) << 2) | (f >> 6);
            d = f & 63;
            if (isNaN(h)) {
                e = d = 64
            } else {
                if (isNaN(f)) {
                    d = 64
                }
            }
            a = a + LZString._keyStr.charAt(j) + LZString._keyStr.charAt(g) + LZString._keyStr.charAt(e) + LZString._keyStr.charAt(d)
        }
        return a
    },
    compress: function(e) {
        if (e == null) {
            return ""
        }
        var h, l, n = {}, m = {}, o = "", c = "", r = "", d = 2, g = 3, b = 2, q = "", a = 0, j = 0, p, k = LZString._f;
        for (p = 0; p < e.length; p += 1) {
            o = e.charAt(p);
            if (!Object.prototype.hasOwnProperty.call(n, o)) {
                n[o] = g++;
                m[o] = true
            }
            c = r + o;
            if (Object.prototype.hasOwnProperty.call(n, c)) {
                r = c
            } else {
                if (Object.prototype.hasOwnProperty.call(m, r)) {
                    if (r.charCodeAt(0) < 256) {
                        for (h = 0; h < b; h++) {
                            a = (a << 1);
                            if (j == 15) {
                                j = 0;
                                q += k(a);
                                a = 0
                            } else {
                                j++
                            }
                        }
                        l = r.charCodeAt(0);
                        for (h = 0; h < 8; h++) {
                            a = (a << 1) | (l & 1);
                            if (j == 15) {
                                j = 0;
                                q += k(a);
                                a = 0
                            } else {
                                j++
                            }
                            l = l >> 1
                        }
                    } else {
                        l = 1;
                        for (h = 0; h < b; h++) {
                            a = (a << 1) | l;
                            if (j == 15) {
                                j = 0;
                                q += k(a);
                                a = 0
                            } else {
                                j++
                            }
                            l = 0
                        }
                        l = r.charCodeAt(0);
                        for (h = 0; h < 16; h++) {
                            a = (a << 1) | (l & 1);
                            if (j == 15) {
                                j = 0;
                                q += k(a);
                                a = 0
                            } else {
                                j++
                            }
                            l = l >> 1
                        }
                    }
                    d--;
                    if (d == 0) {
                        d = Math.pow(2, b);
                        b++
                    }
                    delete m[r]
                } else {
                    l = n[r];
                    for (h = 0; h < b; h++) {
                        a = (a << 1) | (l & 1);
                        if (j == 15) {
                            j = 0;
                            q += k(a);
                            a = 0
                        } else {
                            j++
                        }
                        l = l >> 1
                    }
                }
                d--;
                if (d == 0) {
                    d = Math.pow(2, b);
                    b++
                }
                n[c] = g++;
                r = String(o)
            }
        }
        if (r !== "") {
            if (Object.prototype.hasOwnProperty.call(m, r)) {
                if (r.charCodeAt(0) < 256) {
                    for (h = 0; h < b; h++) {
                        a = (a << 1);
                        if (j == 15) {
                            j = 0;
                            q += k(a);
                            a = 0
                        } else {
                            j++
                        }
                    }
                    l = r.charCodeAt(0);
                    for (h = 0; h < 8; h++) {
                        a = (a << 1) | (l & 1);
                        if (j == 15) {
                            j = 0;
                            q += k(a);
                            a = 0
                        } else {
                            j++
                        }
                        l = l >> 1
                    }
                } else {
                    l = 1;
                    for (h = 0; h < b; h++) {
                        a = (a << 1) | l;
                        if (j == 15) {
                            j = 0;
                            q += k(a);
                            a = 0
                        } else {
                            j++
                        }
                        l = 0
                    }
                    l = r.charCodeAt(0);
                    for (h = 0; h < 16; h++) {
                        a = (a << 1) | (l & 1);
                        if (j == 15) {
                            j = 0;
                            q += k(a);
                            a = 0
                        } else {
                            j++
                        }
                        l = l >> 1
                    }
                }
                d--;
                if (d == 0) {
                    d = Math.pow(2, b);
                    b++
                }
                delete m[r]
            } else {
                l = n[r];
                for (h = 0; h < b; h++) {
                    a = (a << 1) | (l & 1);
                    if (j == 15) {
                        j = 0;
                        q += k(a);
                        a = 0
                    } else {
                        j++
                    }
                    l = l >> 1
                }
            }
            d--;
            if (d == 0) {
                d = Math.pow(2, b);
                b++
            }
        }
        l = 2;
        for (h = 0; h < b; h++) {
            a = (a << 1) | (l & 1);
            if (j == 15) {
                j = 0;
                q += k(a);
                a = 0
            } else {
                j++
            }
            l = l >> 1
        }
        while (true) {
            a = (a << 1);
            if (j == 15) {
                q += k(a);
                break
            } else {
                j++
            }
        }
        return q
    },
};
// "0-KNheerqqbRrNm4mnBdRNOUYhY1e7KxtLD6A1DY+tO30="
// 接收进程传递的参数
// var json_parameter = process.argv.splice(2)[0];
String.format = function ()
{
    var param = [];
    for (var i = 0, l = arguments.length; i < l; i++)
    {
        param.push(arguments[i]);
    }
    var statment = param[0]; // get the first element(the original statement)
    param.shift(); // remove the first element from array
    return statment.replace(/\{(\d+)\}/g, function(m, n)
    {
        return param[n];
    });
};
// 用于命令行传递两个参数使用
var page_num = process.argv[2];
var qi = process.argv[3];
// 判断参数是否为 0
if (page_num === 0){

    var json_parameter = String.format('{"type":"brand","la":"en","qi":"{1}","queue":1,"_":"8810"}',qi);
}
else {

    var json_parameter = String.format('{"p":{"start":{0}},"s":{"dis":"flow"},"type":"brand","la":"en","qi":"{1}","queue":1,"_":"8810"}',page_num,qi);
}
// var json_parameter = String.format('{"p":{"start":{0}},"s":{"dis":"flow"},"type":"brand","la":"en","qi":"{1}","queue":1,"_":"8742"}',page_num,qi);
var r = LZString.compressToBase64(json_parameter);
//console.log(json_parameter);
console.log(r);

// N4IgDiBcoM4C4EMBOcoGYAMBfANCGUoAJgJYGQgBmANgPYDuIuIcAnmAKZQgBGSCAOyIg81BNw4CRIAI4luGALQBpAHIALDhyQyZPAEpJVAWwAsxgQCEi 1QHkAqgE11TgIwcA7MoAecADIAIgBsAIJugU4A1HB2mAC80jIArhypUG54APrcAByepgBMTEAA
// N4IgDiBcoM4C4EMBOcoGYAMBfANCGUoAJgJYGQgBmANgPYDuIuIcAnmAKZQgBGSCAOyIg81BNw4CRIAI4luGALQBpAHIALDhyQyZPAEpJVAWwAsxgQCEi+1QHkAqgE11TgIwcA7MoAecADIAIgBsAIJugU4A1HB2mAC80jIArhypUG54APrcAByepgBMTEAA
// N4IgDiBcoM4C4EMBOcoGYAMBfANCGUoAJgJYGQgBmANgPYDuIuIcAnmAKZQgBGSCAOyIg81BNw4CRIAI4luGALQBpAHIALDhyQyZPAEpJVAWwAsxgQCEi+1QHkAqgE11TgIwcA7MoAecADIAIgBsAIJugU4A1HB2mAC80jIArhypUG54APrcAByepgBMTEAA

/**
 * Created by lee on 17-2-14.
 */
function FrameManager(last, lastL) {
        this.last = last;
        this.lastL = lastL;

        this.splice = function (l, now) {
            if (this.last == now) {
                return;
            }

            var eNow = document.getElementById(now);
            var eLast = document.getElementById(this.last);
            var This = this;
            eNow.style.zIndex = 1;

            $(l.firstElementChild).addClass('active');
            if (this.lastL) {
                $(this.lastL.firstElementChild).removeClass('active');
            }

            var cb = function () {
                eNow.style.zIndex = 2;
                eLast.style.zIndex = 0;
                eLast.style.left = 0;
                This.last = now;
                This.lastL = l;
            };

            $(eLast).animate({left: '-100%'}, 500, cb);
        }

    }
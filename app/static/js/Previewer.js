/**
 * Created by lee on 17-2-13.
 */
function Previewer(view_selector, category, order) {
    this.current_category = category || null;
    this.order = order || null;
    this.view = view_selector;
}


(function () {
    function clickPreview(path, e) {
        //path = '/app/view/article?path=' + path;
        var title = $(e).attr('data-title');

        if (title in localStorage){
            $('#like-icon').attr('class', 'fa fa-heart');
        }else{
            $('#like-icon').attr('class', 'fa fa-heart-o');
        }

        function __animate() {
                var w = $('.aside1').get(0).offsetWidth;
                $('.article-reader').animate({left: 0});
        }

        $(function () {
            $('#loading').fadeIn(300);
            $('#article-content').html("");
            $.ajax({url:path,
                success: function (markdown) {
                    try {
                        testEditormdView = editormd.markdownToHTML("article-content", {
                            markdown: markdown,//+ "\r\n" + $("#append-test").text(),
                           // htmlDecode      : true,       // 开启 HTML 标签解析，为了安全性，默认不开启
                            htmlDecode: "style,script,iframe",  // you can filter tags decode
                            //toc             : false,
                            tocm: true,    // Using [TOCM]
                            emoji: true,
                            taskList: true,
                            tex: true,  // 默认不解析
                            flowChart: true,  // 默认不解析
                            sequenceDiagram: true,  // 默认不解析
                            path: '/static/lib/'
                        });
                    }catch (e){

                    }finally {
                        $('#loading').fadeOut(300);
                        __animate();
                    }
                },
                async:  true,
                cache: false,
                complete: function () {
                    var title = $(e).attr('data-title');
                    $.get("update-reading-counter?title=" + title);
                    var footer = $(e).children('.article-footer').children('span').html()
                    var tags = footer.split("·");
                    var views = parseInt($(e).attr('data-views')) + 1;
                    $(e).attr('data-views', views);
                    $(e).children('.article-footer').children('span').html("阅读&nbsp;" + views + "&nbsp;"+ "·" + tags[1] + "·" + tags[2]);

                    $('.btn-like').attr('data-title', title);
                    $('.btn-like').attr('data-current-id', $(e).attr('id'));
                    $('.btn-like > .like-counter > div').html($(e).attr('data-likes'));
                }
            });
        }());
    }

    Previewer.prototype.getPreviewList = function (offset, count, callBack) {
        offset = offset || 0;
        count = count || 10;

        var url = "post-preview?offset=" + offset + "&count=" + count;
        if (this.current_category){
            url += ("&category=" + encodeURIComponent(this.current_category));
        }

        if (this.order){
            url += ("&order=" + this.order)
        }

        _this = this;
        function __callBack() {
            var children = $(_this.view).children();
            for (var i = 0; i < children.length; ++i){
                (function (j) {
                    $(children[j]).attr('onclick', "");
                    $(children[j]).bind("click", function () {
                        var path = $(children[j]).attr("data-path");
                        clickPreview(path, children[j]);
                    });
                }(i));
            }

            if (callBack){
                callBack();
            }
        }

        $(this.view).load(url, __callBack);
    };

    Previewer.prototype.setOrder = function (order) {
        this.order = order;
    };

    Previewer.prototype.setCurrentCategory = function (category) {
        this.current_category = category;
    }
}());
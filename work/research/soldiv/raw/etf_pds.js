var etfPdsSearch = (function() {
    function search(keyword) {
        $.ajax({
            url : "/api/etf/pds/search",
            data : {
                "keyword": keyword,
            },
            type : "get",
            success: function(res) {
                makeSearchAutoCompleteItem(keyword, res.items);
            },
            error: function () {
                alert("오류가 발생했습니다.");
            }
        });
    }

    function makeSearchAutoCompleteItem(keyword, data) {
        var html = "";

        if(data != null && data.length > 0) {
            $(".related-auto-key").attr("style", "display: block");
            data.forEach(function(item, index) {
                var regex = new RegExp(keyword, 'gi');
                var matches = item.ETF_NAME.match(regex);

                if(matches !=null && matches[0]!=null)
                {
                    item.ETF_NAME = item.ETF_NAME.replace(new RegExp(matches[0], "g"), "<em class=\"highlight\">" + matches[0] + "</em>");
                }
                html += "<button type=\"button\" class=\"item\" onclick=\"document.location.href='/ko/fund/etf/"+item.FUND_CD+"'\">" + item.ETF_NAME + "</button>";
            });
        }
        else {
            $(".related-auto-key").attr("style", "display: none");
        }

        $(".related-auto-key").html(html);
    }

    function assistanceReplace(keyword, text) {
    }

    return {
        search: function(e) {
            if(window.event.keyCode == 13) {
                document.location.href = "./pds?keyword=" + e.value;
            }
            else {
                search(e.value);
            }

        }

    }
})();

var etfPdsPaging = (function() {
    var page = 1;
    var displayedCount = 0;
    var totalCount = 0;

    function more(keyword) {
        $.ajax({
            url : "/api/etf/pds",
            data : {
                "keyword": keyword,
                "page": page,
            },
            type : "get",
            success: function(res) {
                displayedCount += res.items.length;
                totalCount = res.totalCount;
                makeListItem(res.items);
                page++;
            },
            error: function () {
                alert("오류가 발생했습니다.");
            }
        });
    }

    // 더보기 그려주자
    function
    makeMoreButton() {
        var html = "";
        if(displayedCount < totalCount) {
            html = "<button type=\"button\" class=\"btn-list-more\" onclick=\"etfPdsPaging.more();\"><span class=\"ir-a i-arr-4\">더보기 (<span class=\"num\"><em>" + displayedCount + "</em>/" + totalCount + "</span>)</span></button>";
        }

        $(".list-more").html(html);
    }

    // 리스트를 그려주자
    function makeListItem(data) {
        var html = "";

        data.forEach(function(item, index) {
                html += "<tr>\n" +
                        "    <td class=\"al\"><a href=\"/ko/fund/etf/" + item.FUND_CD + "\">" + item.ETF_NAME + "</a></td>\n" +
                        "    <td><button onclick=\"etfPdsPopup.doc0101P('" + item.FUND_CD + "')\" class=\"ir-a i-sch-3\">상세보기</button></td>\n" +
                        "    <td><button onclick=\"etfPdsPopup.doc0102P('" + item.FUND_CD + "')\" class=\"ir-a i-sch-3\">상세보기</button></td>\n" +
                        "    <td><button onclick=\"etfPdsPopup.doc0103P('" + item.FUND_CD + "')\" class=\"ir-a i-sch-3\">상세보기</button></td>\n" +
                        // "    <td class=\"am\"><button class=\"ir-b i-down-2\"><span class=\"blind\">다운로드</span></button></td>\n" +
                        ";</tr>";
        });

        $(".tb-data tbody").append(html);

        makeMoreButton();
    }

    return {
        initialize: function() {
            page = 1;
            displayedCount = 0;
            totalCount = 0;
        },
        more: function(keyword) {
            more(keyword);
        }
    }
})();

var etfPdsPopup = (function() {
    function makeDoc0101pContent(fundCode) {
        var contentTop = "";
        var contentHeader = "<div class=\"tb-scroll-y scroll\">\n" +
            "                <table class=\"tb-data ac\">\n" +
            "                    <caption>분배금 현황</caption>\n" +
            "                    <colgroup>\n" +
            "                        <col style=\"width:25%;\" />\n" +
            "                        <col style=\"width:25%;\" />\n" +
            "                        <col style=\"width:25%;\" />\n" +
            "                        <col style=\"width:25%;\" />\n" +
            "                        <col style=\"width:0; display:none;\" />\n" +
            "                        <col style=\"width:0; display:none;\" />\n" +
            "                    </colgroup>\n" +
            "                    <thead>\n" +
            "                    <tr>\n" +
            "                        <th scope=\"col\">지급기준일</th>\n" +
            "                        <th scope=\"col\">실제지급일</th>\n" +
            "                        <th scope=\"col\">분배금액(원)</th>\n" +
            "                        <th scope=\"col\">주당과세표준액(원)</th>\n" +
            "                        <th scope=\"col\" style=\"display:none; width:0;\">과표기준가(원)</th>\n" +
            "                        <th scope=\"col\" style=\"display:none; width:0;\">배당과표기준가(원)</th>\n" +
            "                    </tr>\n" +
            "                    </thead>\n" +
            "                    <tbody>\n";

        var contentBottom = "                    </tbody>\n" +
            "                </table>\n" +
            "            </div>"
            "            </div>";

        var content = "";
        $.ajax({
            url : "/api/etf/pds/dividend/" + fundCode,
            type: "get",
            success: function(data) {

                contentTop = "<div class=\"pop-cont-in\">\n" +
                    "                <div class=\"g-head-p cmg\">\n" +
                    "                    <h3 class=\"g-title-p\">" + data.fundName + "</h3>\n" +
                    // "                    <div class=\"g-side-txt\"><strong class=\"fc-4\">" + data.workDt.substring(0, 4) + "년 "+ data.workDt.substring(4, 6) +"월 "+data.workDt.substring(6, 8)+"일 기준 반영</strong></div>\n" +
                    "                </div>\n" +
                    "\n" +
                    "                <!-- 리스트 정렬 (s) // -->\n" +
                    "                <div class=\"list-opt-sorting mgt-40\">\n" +
                    "                    <div class=\"list-sort-txt\">\n" +
                    "                        <div class=\"list-total\">\n" +
                    "                            총 <em class=\"num\">" + three_commas(data.totalCount)+"</em>건\n" +
                    "                        </div>\n" +
                    "                    </div>\n" +
                    "                    <div class=\"list-sort-etc\">\n" +
                    "                        <a href=\"/api/etf/pds/down/dividend/" + fundCode + "\" class=\"ir-b i-down api-download-btn\">엑셀 다운로드</a>\n" +
                    "                    </div>\n" +
                    "                </div>\n" +
                    "                <!-- // (e) 리스트 정렬 -->\n";
                if(data.items.length > 0) {
                    data.items.forEach(function (item, index) {
                        content += "<tr>" +
                            "<td>" + item.WORK_DT.substring(0, 4) + "." + item.WORK_DT.substring(4, 6) + "." + item.WORK_DT.substring(6, 8) + "</td>" +
                            "<td>" + item.DIVIDEND_DT.substring(0, 4) + "." + item.DIVIDEND_DT.substring(4, 6) + "." + item.DIVIDEND_DT.substring(6, 8) + "</td>" +
                            "<td>" + three_commas(item.DIVIDEND_PRI) + "</td>" +
                            "<td>" + three_commas(item.WEEK_PRI) + "</td>" +
                            "<td style=\"display:none;\">" + (item.TAX_PRI !== null ? three_commas(item.TAX_PRI) : '-') + "</td>" +
                            "<td style=\"display:none;\">" + (item.BFAS_STAS_STPR !== null ? three_commas(item.BFAS_STAS_STPR) : '-') + "</td>" +
                            "</tr>";
                    });
                }else{
                    content += "<tr><td colspan='6'>분배금 현황이 없습니다</td></tr>";
                }

                $("#SEPC_DOC_01_01P .pop-contents").html(contentTop + contentHeader + content + contentBottom);
                // 과표기준가, 배당과표기준가 열 숨김 처리
                $("#SEPC_DOC_01_01P table.tb-data th:nth-child(5), #SEPC_DOC_01_01P table.tb-data th:nth-child(6)").hide();
                $("#SEPC_DOC_01_01P table.tb-data td:nth-child(5), #SEPC_DOC_01_01P table.tb-data td:nth-child(6)").hide();
                $("#SEPC_DOC_01_01P").uipop('open');

            },
            error: function() {
                alert("오류가 발생했습니다.");
            }
        });
    }

    function makeDoc0102pContent(fundCode) {
        var contentTop = "";
        var contentHeader = "\t\t\t\t<table class=\"tb-data ac\">\n" +
            "\t\t\t\t\t<caption>구성종목(PDF) 현황</caption>\n" +
            "\t\t\t\t\t<colgroup>" +
            "<col style=\"width:10%;\" />" +
            // "<col style=\"width:15%;\" />" +
            "<col />" +
            "<col style=\"width:15%;\" />" +
            "<col style=\"width:22.5%;\" />" +
            "<col style=\"width:15%;\" />" +
            "</colgroup>\n" +
            "\t\t\t\t\t<thead>\n" +
            "\t\t\t\t\t<tr>\n" +
            "\t\t\t\t\t\t<th scope=\"col\">No.</th>\n" +
            // "\t\t\t\t\t\t<th scope=\"col\">종목코드</th>\n" +
            "\t\t\t\t\t\t<th scope=\"col\">종목명</th>\n" +
            "\t\t\t\t\t\t<th scope=\"col\">수량(주)</th>\n" +
            "\t\t\t\t\t\t<th scope=\"col\">평가금액(원)</th>\n" +
            "\t\t\t\t\t\t<th scope=\"col\">비중(%)</th>\n" +
            "\t\t\t\t\t</tr>\n" +
            "\t\t\t\t\t</thead>\n" +
            "\t\t\t\t\t<tbody>\n";

        var contentBottom = "\t\t\t\t\t</tbody>\n" +
            "\t\t\t\t</table>\n" +
            "\t\t\t</div>";

        var content = "";

        $.ajax({
            url : "/api/etf/pds/pdf/" + fundCode,
            type: "get",
            success: function(data) {

                if(data.items.length > 0) {
                    contentTop = "<div class=\"pop-cont-in\">\n" +
                        "\t\t\t\t<div class=\"g-head-p cmg\">\n" +
                        "\t\t\t\t\t<h3 class=\"g-title-p\">" + data.fundName + "</h3>\n" +
                        "\t\t\t\t\t<div class=\"g-side-txt\"><strong class=\"fc-4\">" + data.workDt.substring(0, 4) + "년 "+ data.workDt.substring(4, 6) +"월 "+data.workDt.substring(6, 8)+"일 기준</strong></div>\n" +
                        "\t\t\t\t</div>\n" +
                        "\n" +
                        "\t\t\t\t<!-- 리스트 정렬 (s) // -->\n" +
                        "\t\t\t\t<div class=\"list-opt-sorting mgt-40\">\n" +
                        "\t\t\t\t\t<div class=\"list-sort-txt\">\n" +
                        "\t\t\t\t\t\t<div class=\"list-total\">\n" +
                        "\t\t\t\t\t\t\t총 <em class=\"num\">" + data.totalCount+"</em>건\n" +
                        "\t\t\t\t\t\t</div>\n" +
                        "\t\t\t\t\t</div>\n" +
                        "\t\t\t\t\t<div class=\"list-sort-etc\">\n" +
                        "\t\t\t\t\t\t<a href=\"/api/etf/pds/down/pdf/" + fundCode + "\" class=\"ir-b i-down api-download-btn\">엑셀 다운로드</a>\n" +
                        "\t\t\t\t\t</div>\n" +
                        "\t\t\t\t</div>\n" +
                        "\t\t\t\t<!-- // (e) 리스트 정렬 -->\n" +
                        "\n";

                    data.items.forEach(function (item, index) {
                        content += "<tr>" +
                            "<td>" + (index + 1) + "</td>" +
                            // "<td>" + item.FUND_CD + "</td>" +
                            "<td>" + item.SEC_NM + "</td>" +
                            "<td>" + three_commas(item.QTY) + "</td>" +
                            "<td>" + three_commas(item.PRICE) + "</td>" +
                            "<td>" + item.WT_DISP + "</td>" +
                            "</tr>";
                    });
                }else{
                    contentTop = "<div class=\"pop-cont-in\">\n" +
                        "\t\t\t\t<div class=\"g-head-p cmg\">\n" +
                        "\t\t\t\t\t<h3 class=\"g-title-p\">" + data.fundName + "</h3>\n" +
                        "\t\t\t\t</div>\n" +
                        "\n" +
                        "\t\t\t\t<!-- 리스트 정렬 (s) // -->\n" +
                        "\t\t\t\t<div class=\"list-opt-sorting mgt-40\">\n" +
                        "\t\t\t\t\t<div class=\"list-sort-txt\">\n" +
                        "\t\t\t\t\t\t<div class=\"list-total\">\n" +
                        "\t\t\t\t\t\t\t총 <em class=\"num\">" + data.totalCount+"</em>건\n" +
                        "\t\t\t\t\t\t</div>\n" +
                        "\t\t\t\t\t</div>\n" +
                        "\t\t\t\t\t<div class=\"list-sort-etc\">\n" +
                        "\t\t\t\t\t\t<a href=\"/api/etf/pds/down/pdf/" + fundCode + "\" class=\"ir-b i-down api-download-btn\">엑셀 다운로드</a>\n" +
                        "\t\t\t\t\t</div>\n" +
                        "\t\t\t\t</div>\n" +
                        "\t\t\t\t<!-- // (e) 리스트 정렬 -->\n" +
                        "\n";

                    content += "<tr><td colspan='5'>구성종목 현황이 없습니다</td></tr>";
                }

                $("#SEPC_DOC_01_02P .pop-contents").html(contentTop + contentHeader + content + contentBottom);
                $("#SEPC_DOC_01_02P").uipop('open');

            },
            error: function() {
                alert("오류가 발생했습니다.");
            }
        });
    }

    function makeDoc0103pContent(fundCode) {
        var content = "";

        $.ajax({
            url : "/api/etf/pds/policyDescription/" + fundCode,
            type: "get",
            success: function(data) {
                if(data) {
                    content = "<div class=\"pop-cont-in\">\n" +
                        "\t\t\t\t<h3 class=\"g-title-p cmg\">" + data.FUND_NM + "</h3>\n" +
                        "\n" +
                        "\t\t\t\t<table class=\"tb-data ac\">\n" +
                        "\t\t\t\t\t<caption>규약/투자설명서</caption>\n" +
                        "\t\t\t\t\t<colgroup><col span=\"3\" style=\"width:33.33%;\" /></colgroup>\n" +
                        "\t\t\t\t\t<thead>\n" +
                        "\t\t\t\t\t\t<tr>\n" +
                        "\t\t\t\t\t\t\t<th scope=\"col\">투자설명서</th>\n" +
                        "\t\t\t\t\t\t\t<th scope=\"col\">집합규약설명서</th>\n" +
                        "\t\t\t\t\t\t\t<th scope=\"col\">간이투자설명서</th>\n" +
                        "\t\t\t\t\t\t</tr>\n" +
                        "\t\t\t\t\t</thead>\n" +
                        "\t\t\t\t\t<tbody>\n" +
                        "\t\t\t\t\t\t<!-- # item // # -->\n" +
                        "\t\t\t\t\t\t<tr>\n" +
                        "\t\t\t\t\t\t\t<td><a href=\"/api/etf/pds/down/policyDescription/" + data.FUND_CD + "?type=description\" class=\"ir-b i-down api-download-btn\">다운로드</a></td>\n" +
                        "\t\t\t\t\t\t\t<td><a href=\"/api/etf/pds/down/policyDescription/" + data.FUND_CD + "?type=policy\" class=\"ir-b i-down api-download-btn\">다운로드</a></td>\n" +
                        "\t\t\t\t\t\t\t<td><a href=\"/api/etf/pds/down/policyDescription/" + data.FUND_CD + "?type=simple_desc\" class=\"ir-b i-down api-download-btn\">다운로드</a></td>\n" +
                        "\t\t\t\t\t\t</tr>\n" +
                        "\t\t\t\t\t\t<!-- # // item # -->\n" +
                        "\n" +
                        "\t\t\t\t\t</tbody>\n" +
                        "\t\t\t\t</table>\n" +
                        "\n" +
                        "\t\t\t\t<dl class=\"dot-list mgt-70\">\n" +
                        "\t\t\t\t\t<dt class=\"ir-b i-mark-3\">참고하세요</dt>\n" +
                        "\t\t\t\t\t<dd>본 웹사에트에서 제공하는 지수 및 수익률 정보는 투자 참고사항이며, 오류가 발생하거나 지연될 수 있습니다.</dd>\n" +
                        "\t\t\t\t\t<dd>제공된 정보에 의한 투자결과에 대한 법적인 책임을 지지 않습니다.(지수정보는 코스콤으로부터 제공받고 있습니다.)</dd>\n" +
                        "\t\t\t\t\t<dd>가입하시기 전에 투자대상, 환매방법 및 보수 등에 관하여 투자설명서를 받으시 읽어보시기 바랍니다.<br />집합투자상품은 운용결과에 따른 이익 또는 손실이 투자자에게 귀속됩니다.</dd>\n" +
                        "\t\t\t\t</dl>\n" +
                        "\t\t\t</div>";

                    $("#SEPC_DOC_01_03P .pop-contents").html(content);
                    $("#SEPC_DOC_01_03P").uipop('open');
                }
                else {
                    alert("데이터가 없습니다.");
                }
            },
            error: function() {
                alert("오류가 발생했습니다.");
            }
        });
    }

    return {
        doc0101P : function(fundCode) {
            makeDoc0101pContent(fundCode);
        },
        doc0102P : function(fundCode) {
            makeDoc0102pContent(fundCode);
        },
        doc0103P : function(fundCode) {
            makeDoc0103pContent(fundCode);
        },
    }
})();
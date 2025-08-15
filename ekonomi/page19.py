from streamlit_echarts import st_echarts
import streamlit as st


options = {
    "title": {"text": "某站点用户访问来源", "subtext": "纯属虚构", "left": "center"},
    "tooltip": {"trigger": "item"},
    "legend": {
        "orient": "vertical",
        "left": "left",
    },
    "series": [
        {
            "name": "访问来源",
            "type": "pie",
            "radius": "50%",
            "data": [
                {"value": 1048, "name": "搜索引擎"},
                {"value": 735, "name": "直接访问"},
                {"value": 580, "name": "邮件营销"},
                {"value": 484, "name": "联盟广告"},
                {"value": 300, "name": "视频广告"},
            ],
            "emphasis": {
                "itemStyle": {
                    "shadowBlur": 10,
                    "shadowOffsetX": 0,
                    "shadowColor": "rgba(0, 0, 0, 0.5)",
                }
            },
        }
    ],
}
st.markdown("Select a legend, see the detail")
events = {
    "legendselectchanged": "function(params) { return params.selected }",
}
s = st_echarts(
    options=options, events=events, height="600px", key="render_pie_events"
)
if s is not None:
    st.write(s)
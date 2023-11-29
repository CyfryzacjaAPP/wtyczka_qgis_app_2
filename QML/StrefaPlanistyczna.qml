<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis styleCategories="Symbology|Symbology3D|Labeling|Fields|Forms|Actions|MapTips|Diagrams|AttributeTable|Rendering|CustomProperties|GeometryOptions|Relations|Temporal|Legend|Elevation|Notes" simplifyAlgorithm="0" labelsEnabled="1" simplifyLocal="1" simplifyDrawingTol="2" maxScale="0" simplifyMaxScale="1" version="3.22.15-Białowieża" hasScaleBasedVisibilityFlag="0" minScale="100000000" simplifyDrawingHints="0" symbologyReferenceScale="-1">
  <temporal durationField="fid" durationUnit="min" fixedDuration="0" mode="0" limitMode="0" startField="" accumulate="0" enabled="0" startExpression="" endField="" endExpression="">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <renderer-v2 enableorderby="0" symbollevels="0" type="singleSymbol" forceraster="0" referencescale="-1">
    <symbols>
      <symbol name="0" alpha="1" type="fill" force_rhr="0" clip_to_extent="1">
        <data_defined_properties>
          <Option type="Map">
            <Option name="name" value="" type="QString"/>
            <Option name="properties"/>
            <Option name="type" value="collection" type="QString"/>
          </Option>
        </data_defined_properties>
        <layer class="SimpleFill" enabled="1" locked="0" pass="0">
          <Option type="Map">
            <Option name="border_width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="color" value="189,189,189,255" type="QString"/>
            <Option name="joinstyle" value="bevel" type="QString"/>
            <Option name="offset" value="0,0" type="QString"/>
            <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="offset_unit" value="MM" type="QString"/>
            <Option name="outline_color" value="35,35,35,255" type="QString"/>
            <Option name="outline_style" value="no" type="QString"/>
            <Option name="outline_width" value="0.5" type="QString"/>
            <Option name="outline_width_unit" value="MM" type="QString"/>
            <Option name="style" value="solid" type="QString"/>
          </Option>
          <prop v="3x:0,0,0,0,0,0" k="border_width_map_unit_scale"/>
          <prop v="189,189,189,255" k="color"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="35,35,35,255" k="outline_color"/>
          <prop v="no" k="outline_style"/>
          <prop v="0.5" k="outline_width"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="solid" k="style"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="fillColor" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="CASE&#xd;&#xa;WHEN  &quot;symbol&quot; = 'SW' THEN color_rgb(184,149,120)&#xd;&#xa;WHEN  &quot;symbol&quot; = 'SJ' THEN color_rgb(238,201,122)&#xd;&#xa;WHEN  &quot;symbol&quot; = 'SZ' THEN color_rgb(254,232,139)&#xd;&#xa;WHEN  &quot;symbol&quot; = 'SU' THEN color_rgb(255,170,153)&#xd;&#xa;WHEN  &quot;symbol&quot; = 'SH' THEN color_rgb(255,147,211)&#xd;&#xa;WHEN  &quot;symbol&quot; = 'SP' THEN color_rgb(197,144,222)&#xd;&#xa;WHEN  &quot;symbol&quot; = 'SR' THEN color_rgb(254,188,122)&#xd;&#xa;WHEN  &quot;symbol&quot; = 'SI' THEN color_rgb(204,204,204)&#xd;&#xa;WHEN  &quot;symbol&quot; = 'SN' THEN color_rgb(187,245,139)&#xd;&#xa;WHEN  &quot;symbol&quot; = 'SC' THEN color_rgb(148,212,196)&#xd;&#xa;WHEN  &quot;symbol&quot; = 'SG' THEN color_rgb(252,204,255)&#xd;&#xa;WHEN  &quot;symbol&quot; = 'SO' THEN color_rgb(240,255,204)&#xd;&#xa;WHEN  &quot;symbol&quot; = 'SK' THEN color_rgb(242,242,242)&#xd;&#xa;END" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer class="SimpleLine" enabled="1" locked="0" pass="0">
          <Option type="Map">
            <Option name="align_dash_pattern" value="0" type="QString"/>
            <Option name="capstyle" value="square" type="QString"/>
            <Option name="customdash" value="13.5;4.5" type="QString"/>
            <Option name="customdash_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="customdash_unit" value="MM" type="QString"/>
            <Option name="dash_pattern_offset" value="0" type="QString"/>
            <Option name="dash_pattern_offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="dash_pattern_offset_unit" value="MM" type="QString"/>
            <Option name="draw_inside_polygon" value="0" type="QString"/>
            <Option name="joinstyle" value="miter" type="QString"/>
            <Option name="line_color" value="83,83,83,255" type="QString"/>
            <Option name="line_style" value="solid" type="QString"/>
            <Option name="line_width" value="0.5" type="QString"/>
            <Option name="line_width_unit" value="MM" type="QString"/>
            <Option name="offset" value="0" type="QString"/>
            <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="offset_unit" value="MM" type="QString"/>
            <Option name="ring_filter" value="0" type="QString"/>
            <Option name="trim_distance_end" value="0" type="QString"/>
            <Option name="trim_distance_end_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="trim_distance_end_unit" value="MM" type="QString"/>
            <Option name="trim_distance_start" value="0" type="QString"/>
            <Option name="trim_distance_start_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="trim_distance_start_unit" value="MM" type="QString"/>
            <Option name="tweak_dash_pattern_on_corners" value="0" type="QString"/>
            <Option name="use_custom_dash" value="0" type="QString"/>
            <Option name="width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
          </Option>
          <prop v="0" k="align_dash_pattern"/>
          <prop v="square" k="capstyle"/>
          <prop v="13.5;4.5" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="dash_pattern_offset"/>
          <prop v="3x:0,0,0,0,0,0" k="dash_pattern_offset_map_unit_scale"/>
          <prop v="MM" k="dash_pattern_offset_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="miter" k="joinstyle"/>
          <prop v="83,83,83,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.5" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="trim_distance_end"/>
          <prop v="3x:0,0,0,0,0,0" k="trim_distance_end_map_unit_scale"/>
          <prop v="MM" k="trim_distance_end_unit"/>
          <prop v="0" k="trim_distance_start"/>
          <prop v="3x:0,0,0,0,0,0" k="trim_distance_start_map_unit_scale"/>
          <prop v="MM" k="trim_distance_start_unit"/>
          <prop v="0" k="tweak_dash_pattern_on_corners"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="outlineWidth" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="if (@zoom_level &lt; 15,0.25,0.5)" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <labeling type="simple">
    <settings calloutType="simple">
      <text-style fontFamily="Arial" isExpression="0" textOrientation="horizontal" fontKerning="1" fontSizeMapUnitScale="3x:0,0,0,0,0,0" fieldName="oznaczenie" blendMode="0" capitalization="0" useSubstitutions="0" fontLetterSpacing="0" fontWeight="50" fontSize="3" fontUnderline="0" fontSizeUnit="MM" fontWordSpacing="0" previewBkgrdColor="255,255,255,255" textColor="0,0,0,255" namedStyle="Normal" textOpacity="1" legendString="Aa" fontItalic="0" allowHtml="0" multilineHeight="1" fontStrikeout="0">
        <families/>
        <text-buffer bufferSizeUnits="MM" bufferDraw="1" bufferJoinStyle="128" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferColor="255,255,255,255" bufferNoFill="1" bufferOpacity="1" bufferSize="0.5" bufferBlendMode="0"/>
        <text-mask maskSize="0" maskEnabled="0" maskJoinStyle="128" maskSizeMapUnitScale="3x:0,0,0,0,0,0" maskSizeUnits="MM" maskedSymbolLayers="" maskType="0" maskOpacity="1"/>
        <background shapeFillColor="255,255,255,255" shapeType="0" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeJoinStyle="64" shapeRotationType="0" shapeOffsetX="0" shapeSizeUnit="Point" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeRadiiX="0" shapeRadiiUnit="Point" shapeOpacity="1" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeSizeY="0" shapeBorderWidthUnit="Point" shapeSVGFile="" shapeRadiiY="0" shapeOffsetUnit="Point" shapeSizeType="0" shapeBorderColor="128,128,128,255" shapeBlendMode="0" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeDraw="0" shapeBorderWidth="0" shapeRotation="0" shapeOffsetY="0" shapeSizeX="0">
          <symbol name="markerSymbol" alpha="1" type="marker" force_rhr="0" clip_to_extent="1">
            <data_defined_properties>
              <Option type="Map">
                <Option name="name" value="" type="QString"/>
                <Option name="properties"/>
                <Option name="type" value="collection" type="QString"/>
              </Option>
            </data_defined_properties>
            <layer class="SimpleMarker" enabled="1" locked="0" pass="0">
              <Option type="Map">
                <Option name="angle" value="0" type="QString"/>
                <Option name="cap_style" value="square" type="QString"/>
                <Option name="color" value="183,72,75,255" type="QString"/>
                <Option name="horizontal_anchor_point" value="1" type="QString"/>
                <Option name="joinstyle" value="bevel" type="QString"/>
                <Option name="name" value="circle" type="QString"/>
                <Option name="offset" value="0,0" type="QString"/>
                <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="offset_unit" value="MM" type="QString"/>
                <Option name="outline_color" value="35,35,35,255" type="QString"/>
                <Option name="outline_style" value="solid" type="QString"/>
                <Option name="outline_width" value="0" type="QString"/>
                <Option name="outline_width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="outline_width_unit" value="MM" type="QString"/>
                <Option name="scale_method" value="diameter" type="QString"/>
                <Option name="size" value="2" type="QString"/>
                <Option name="size_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="size_unit" value="MM" type="QString"/>
                <Option name="vertical_anchor_point" value="1" type="QString"/>
              </Option>
              <prop v="0" k="angle"/>
              <prop v="square" k="cap_style"/>
              <prop v="183,72,75,255" k="color"/>
              <prop v="1" k="horizontal_anchor_point"/>
              <prop v="bevel" k="joinstyle"/>
              <prop v="circle" k="name"/>
              <prop v="0,0" k="offset"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="35,35,35,255" k="outline_color"/>
              <prop v="solid" k="outline_style"/>
              <prop v="0" k="outline_width"/>
              <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
              <prop v="MM" k="outline_width_unit"/>
              <prop v="diameter" k="scale_method"/>
              <prop v="2" k="size"/>
              <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
              <prop v="MM" k="size_unit"/>
              <prop v="1" k="vertical_anchor_point"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" value="" type="QString"/>
                  <Option name="properties"/>
                  <Option name="type" value="collection" type="QString"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
          <symbol name="fillSymbol" alpha="1" type="fill" force_rhr="0" clip_to_extent="1">
            <data_defined_properties>
              <Option type="Map">
                <Option name="name" value="" type="QString"/>
                <Option name="properties"/>
                <Option name="type" value="collection" type="QString"/>
              </Option>
            </data_defined_properties>
            <layer class="SimpleFill" enabled="1" locked="0" pass="0">
              <Option type="Map">
                <Option name="border_width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="color" value="255,255,255,255" type="QString"/>
                <Option name="joinstyle" value="bevel" type="QString"/>
                <Option name="offset" value="0,0" type="QString"/>
                <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="offset_unit" value="MM" type="QString"/>
                <Option name="outline_color" value="128,128,128,255" type="QString"/>
                <Option name="outline_style" value="no" type="QString"/>
                <Option name="outline_width" value="0" type="QString"/>
                <Option name="outline_width_unit" value="Point" type="QString"/>
                <Option name="style" value="solid" type="QString"/>
              </Option>
              <prop v="3x:0,0,0,0,0,0" k="border_width_map_unit_scale"/>
              <prop v="255,255,255,255" k="color"/>
              <prop v="bevel" k="joinstyle"/>
              <prop v="0,0" k="offset"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="128,128,128,255" k="outline_color"/>
              <prop v="no" k="outline_style"/>
              <prop v="0" k="outline_width"/>
              <prop v="Point" k="outline_width_unit"/>
              <prop v="solid" k="style"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" value="" type="QString"/>
                  <Option name="properties"/>
                  <Option name="type" value="collection" type="QString"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </background>
        <shadow shadowOpacity="0.69999999999999996" shadowOffsetAngle="135" shadowScale="100" shadowUnder="0" shadowRadiusUnit="MM" shadowDraw="0" shadowRadiusAlphaOnly="0" shadowColor="0,0,0,255" shadowBlendMode="6" shadowOffsetGlobal="1" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowOffsetDist="1" shadowRadius="1.5" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowOffsetUnit="MM"/>
        <dd_properties>
          <Option type="Map">
            <Option name="name" value="" type="QString"/>
            <Option name="properties"/>
            <Option name="type" value="collection" type="QString"/>
          </Option>
        </dd_properties>
        <substitutions/>
      </text-style>
      <text-format rightDirectionSymbol=">" decimals="3" leftDirectionSymbol="&lt;" formatNumbers="0" wrapChar="" useMaxLineLengthForAutoWrap="1" multilineAlign="3" addDirectionSymbol="0" plussign="0" autoWrapLength="0" reverseDirectionSymbol="0" placeDirectionSymbol="0"/>
      <placement layerType="PolygonGeometry" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" offsetUnits="MM" maxCurvedCharAngleOut="-25" polygonPlacementFlags="2" repeatDistanceUnits="MM" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" xOffset="0" overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" geometryGenerator="" distUnits="MM" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" preserveRotation="1" repeatDistance="0" yOffset="0" centroidWhole="0" placement="0" centroidInside="1" rotationUnit="AngleDegrees" dist="0" offsetType="0" priority="10" overrunDistanceUnit="MM" lineAnchorType="0" distMapUnitScale="3x:0,0,0,0,0,0" maxCurvedCharAngleIn="25" lineAnchorPercent="0.5" lineAnchorClipping="0" quadOffset="4" placementFlags="10" rotationAngle="0" fitInPolygonOnly="0" geometryGeneratorEnabled="0" geometryGeneratorType="PointGeometry" overrunDistance="0"/>
      <rendering fontMinPixelSize="3" mergeLines="0" drawLabels="1" limitNumLabels="0" unplacedVisibility="0" maxNumLabels="2000" scaleMax="0" displayAll="0" obstacle="1" upsidedownLabels="0" fontLimitPixelSize="0" obstacleFactor="1" labelPerPart="0" obstacleType="1" fontMaxPixelSize="10000" scaleMin="0" scaleVisibility="0" minFeatureSize="0" zIndex="0"/>
      <dd_properties>
        <Option type="Map">
          <Option name="name" value="" type="QString"/>
          <Option name="properties" type="Map">
            <Option name="Size" type="Map">
              <Option name="active" value="true" type="bool"/>
              <Option name="expression" value="if (@zoom_level &lt; 15,0,3)" type="QString"/>
              <Option name="type" value="3" type="int"/>
            </Option>
          </Option>
          <Option name="type" value="collection" type="QString"/>
        </Option>
      </dd_properties>
      <callout type="simple">
        <Option type="Map">
          <Option name="anchorPoint" value="pole_of_inaccessibility" type="QString"/>
          <Option name="blendMode" value="0" type="int"/>
          <Option name="ddProperties" type="Map">
            <Option name="name" value="" type="QString"/>
            <Option name="properties"/>
            <Option name="type" value="collection" type="QString"/>
          </Option>
          <Option name="drawToAllParts" value="false" type="bool"/>
          <Option name="enabled" value="0" type="QString"/>
          <Option name="labelAnchorPoint" value="point_on_exterior" type="QString"/>
          <Option name="lineSymbol" value="&lt;symbol name=&quot;symbol&quot; alpha=&quot;1&quot; type=&quot;line&quot; force_rhr=&quot;0&quot; clip_to_extent=&quot;1&quot;>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option name=&quot;name&quot; value=&quot;&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option name=&quot;type&quot; value=&quot;collection&quot; type=&quot;QString&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;layer class=&quot;SimpleLine&quot; enabled=&quot;1&quot; locked=&quot;0&quot; pass=&quot;0&quot;>&lt;Option type=&quot;Map&quot;>&lt;Option name=&quot;align_dash_pattern&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;capstyle&quot; value=&quot;square&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;customdash&quot; value=&quot;5;2&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;customdash_map_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;customdash_unit&quot; value=&quot;MM&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;dash_pattern_offset&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;dash_pattern_offset_map_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;dash_pattern_offset_unit&quot; value=&quot;MM&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;draw_inside_polygon&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;joinstyle&quot; value=&quot;bevel&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;line_color&quot; value=&quot;60,60,60,255&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;line_style&quot; value=&quot;solid&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;line_width&quot; value=&quot;0.3&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;line_width_unit&quot; value=&quot;MM&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;offset&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;offset_map_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;offset_unit&quot; value=&quot;MM&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;ring_filter&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;trim_distance_end&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;trim_distance_end_map_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;trim_distance_end_unit&quot; value=&quot;MM&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;trim_distance_start&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;trim_distance_start_map_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;trim_distance_start_unit&quot; value=&quot;MM&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;tweak_dash_pattern_on_corners&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;use_custom_dash&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;width_map_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot;/>&lt;/Option>&lt;prop v=&quot;0&quot; k=&quot;align_dash_pattern&quot;/>&lt;prop v=&quot;square&quot; k=&quot;capstyle&quot;/>&lt;prop v=&quot;5;2&quot; k=&quot;customdash&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;customdash_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;customdash_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;dash_pattern_offset&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;dash_pattern_offset_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;dash_pattern_offset_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;draw_inside_polygon&quot;/>&lt;prop v=&quot;bevel&quot; k=&quot;joinstyle&quot;/>&lt;prop v=&quot;60,60,60,255&quot; k=&quot;line_color&quot;/>&lt;prop v=&quot;solid&quot; k=&quot;line_style&quot;/>&lt;prop v=&quot;0.3&quot; k=&quot;line_width&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;line_width_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;offset&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;offset_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;offset_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;ring_filter&quot;/>&lt;prop v=&quot;0&quot; k=&quot;trim_distance_end&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;trim_distance_end_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;trim_distance_end_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;trim_distance_start&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;trim_distance_start_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;trim_distance_start_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;tweak_dash_pattern_on_corners&quot;/>&lt;prop v=&quot;0&quot; k=&quot;use_custom_dash&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;width_map_unit_scale&quot;/>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option name=&quot;name&quot; value=&quot;&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option name=&quot;type&quot; value=&quot;collection&quot; type=&quot;QString&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>" type="QString"/>
          <Option name="minLength" value="0" type="double"/>
          <Option name="minLengthMapUnitScale" value="3x:0,0,0,0,0,0" type="QString"/>
          <Option name="minLengthUnit" value="MM" type="QString"/>
          <Option name="offsetFromAnchor" value="0" type="double"/>
          <Option name="offsetFromAnchorMapUnitScale" value="3x:0,0,0,0,0,0" type="QString"/>
          <Option name="offsetFromAnchorUnit" value="MM" type="QString"/>
          <Option name="offsetFromLabel" value="0" type="double"/>
          <Option name="offsetFromLabelMapUnitScale" value="3x:0,0,0,0,0,0" type="QString"/>
          <Option name="offsetFromLabelUnit" value="MM" type="QString"/>
        </Option>
      </callout>
    </settings>
  </labeling>
  <customproperties>
    <Option type="Map">
      <Option name="dualview/previewExpressions" type="List">
        <Option value="&quot;gml_id&quot;" type="QString"/>
      </Option>
      <Option name="embeddedWidgets/count" value="0" type="int"/>
      <Option name="variableNames"/>
      <Option name="variableValues"/>
    </Option>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Histogram">
    <DiagramCategory lineSizeScale="3x:0,0,0,0,0,0" spacingUnitScale="3x:0,0,0,0,0,0" barWidth="5" width="15" enabled="0" labelPlacementMethod="XHeight" height="15" sizeScale="3x:0,0,0,0,0,0" penWidth="0" scaleDependency="Area" showAxis="1" penAlpha="255" minScaleDenominator="0" minimumSize="0" rotationOffset="270" scaleBasedVisibility="0" spacing="5" lineSizeType="MM" diagramOrientation="Up" penColor="#000000" opacity="1" maxScaleDenominator="1e+08" spacingUnit="MM" sizeType="MM" direction="0" backgroundAlpha="255" backgroundColor="#ffffff">
      <fontProperties style="" description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0"/>
      <attribute color="#000000" colorOpacity="1" label="" field=""/>
      <axisSymbol>
        <symbol name="" alpha="1" type="line" force_rhr="0" clip_to_extent="1">
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
          <layer class="SimpleLine" enabled="1" locked="0" pass="0">
            <Option type="Map">
              <Option name="align_dash_pattern" value="0" type="QString"/>
              <Option name="capstyle" value="square" type="QString"/>
              <Option name="customdash" value="5;2" type="QString"/>
              <Option name="customdash_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
              <Option name="customdash_unit" value="MM" type="QString"/>
              <Option name="dash_pattern_offset" value="0" type="QString"/>
              <Option name="dash_pattern_offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
              <Option name="dash_pattern_offset_unit" value="MM" type="QString"/>
              <Option name="draw_inside_polygon" value="0" type="QString"/>
              <Option name="joinstyle" value="bevel" type="QString"/>
              <Option name="line_color" value="35,35,35,255" type="QString"/>
              <Option name="line_style" value="solid" type="QString"/>
              <Option name="line_width" value="0.26" type="QString"/>
              <Option name="line_width_unit" value="MM" type="QString"/>
              <Option name="offset" value="0" type="QString"/>
              <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
              <Option name="offset_unit" value="MM" type="QString"/>
              <Option name="ring_filter" value="0" type="QString"/>
              <Option name="trim_distance_end" value="0" type="QString"/>
              <Option name="trim_distance_end_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
              <Option name="trim_distance_end_unit" value="MM" type="QString"/>
              <Option name="trim_distance_start" value="0" type="QString"/>
              <Option name="trim_distance_start_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
              <Option name="trim_distance_start_unit" value="MM" type="QString"/>
              <Option name="tweak_dash_pattern_on_corners" value="0" type="QString"/>
              <Option name="use_custom_dash" value="0" type="QString"/>
              <Option name="width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            </Option>
            <prop v="0" k="align_dash_pattern"/>
            <prop v="square" k="capstyle"/>
            <prop v="5;2" k="customdash"/>
            <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
            <prop v="MM" k="customdash_unit"/>
            <prop v="0" k="dash_pattern_offset"/>
            <prop v="3x:0,0,0,0,0,0" k="dash_pattern_offset_map_unit_scale"/>
            <prop v="MM" k="dash_pattern_offset_unit"/>
            <prop v="0" k="draw_inside_polygon"/>
            <prop v="bevel" k="joinstyle"/>
            <prop v="35,35,35,255" k="line_color"/>
            <prop v="solid" k="line_style"/>
            <prop v="0.26" k="line_width"/>
            <prop v="MM" k="line_width_unit"/>
            <prop v="0" k="offset"/>
            <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
            <prop v="MM" k="offset_unit"/>
            <prop v="0" k="ring_filter"/>
            <prop v="0" k="trim_distance_end"/>
            <prop v="3x:0,0,0,0,0,0" k="trim_distance_end_map_unit_scale"/>
            <prop v="MM" k="trim_distance_end_unit"/>
            <prop v="0" k="trim_distance_start"/>
            <prop v="3x:0,0,0,0,0,0" k="trim_distance_start_map_unit_scale"/>
            <prop v="MM" k="trim_distance_start_unit"/>
            <prop v="0" k="tweak_dash_pattern_on_corners"/>
            <prop v="0" k="use_custom_dash"/>
            <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
            <data_defined_properties>
              <Option type="Map">
                <Option name="name" value="" type="QString"/>
                <Option name="properties"/>
                <Option name="type" value="collection" type="QString"/>
              </Option>
            </data_defined_properties>
          </layer>
        </symbol>
      </axisSymbol>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings zIndex="0" priority="0" placement="1" dist="0" showAll="1" linePlacementFlags="18" obstacle="0">
    <properties>
      <Option type="Map">
        <Option name="name" value="" type="QString"/>
        <Option name="properties"/>
        <Option name="type" value="collection" type="QString"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions geometryPrecision="0.01" removeDuplicateNodes="0">
    <activeChecks/>
    <checkConfiguration type="Map">
      <Option name="QgsGeometryGapCheck" type="Map">
        <Option name="allowedGapsBuffer" value="0" type="double"/>
        <Option name="allowedGapsEnabled" value="false" type="bool"/>
        <Option name="allowedGapsLayer" value="" type="QString"/>
      </Option>
    </checkConfiguration>
  </geometryOptions>
  <legend showLabelLegend="0" type="default-vector"/>
  <referencedLayers/>
  <fieldConfiguration>
    <field configurationFlags="None" name="fid">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="gml_id">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="przestrzenNazw">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="lokalnyId">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="wersjaId">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option name="allow_null" value="true" type="bool"/>
            <Option name="calendar_popup" value="true" type="bool"/>
            <Option name="display_format" value="yyyyMMddTHHmmss" type="QString"/>
            <Option name="field_format" value="yyyyMMddTHHmmss" type="QString"/>
            <Option name="field_iso_format" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="oznaczenie">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="symbol">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="SW" value="SW" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="SJ" value="SJ" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="SZ" value="SZ" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="SU" value="SU" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="SH" value="SH" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="SP" value="SP" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="SR" value="SR" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="SI" value="SI" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="SN" value="SN" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="SC" value="SC" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="SG" value="SG" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="SO" value="SO" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="SK" value="SK" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="NULL" value="{2839923C-8B7D-419E-B84B-CA2FE9B80EC7}" type="QString"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="charakterUstalenia">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="ogólnie wiążące" value="ogólnie wiążące" type="QString"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="obowiazujeOd">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option name="allow_null" value="true" type="bool"/>
            <Option name="calendar_popup" value="true" type="bool"/>
            <Option name="display_format" value="yyyy-MM-dd" type="QString"/>
            <Option name="field_format" value="yyyy-MM-dd" type="QString"/>
            <Option name="field_iso_format" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="obowiazujeDo">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option name="allow_null" value="true" type="bool"/>
            <Option name="calendar_popup" value="true" type="bool"/>
            <Option name="display_format" value="yyyy-MM-dd" type="QString"/>
            <Option name="field_format" value="yyyy-MM-dd" type="QString"/>
            <Option name="field_iso_format" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="status">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="nieaktualny" value="nieaktualny" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="prawnie wiążący lub realizowany" value="prawnie wiążący lub realizowany" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="w opracowaniu" value="w opracowaniu" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="w trakcie przyjmowania" value="w trakcie przyjmowania" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="wybierz" value="{2839923C-8B7D-419E-B84B-CA2FE9B80EC7}" type="QString"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="poczatekWersjiObiektu">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option name="allow_null" value="true" type="bool"/>
            <Option name="calendar_popup" value="true" type="bool"/>
            <Option name="display_format" value="yyyy-MM-ddTHH:mm:ssZ" type="QString"/>
            <Option name="field_format" value="yyyy-MM-ddTHH:mm:ssZ" type="QString"/>
            <Option name="field_iso_format" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="koniecWersjiObiektu">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option name="allow_null" value="true" type="bool"/>
            <Option name="calendar_popup" value="true" type="bool"/>
            <Option name="display_format" value="yyyy-MM-ddTHH:mm:ssZ" type="QString"/>
            <Option name="field_format" value="yyyy-MM-ddTHH:mm:ssZ" type="QString"/>
            <Option name="field_iso_format" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="plan">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="nazwa">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="strefa wielofunkcyjna z zabudową mieszkaniową wielorodzinną" value="strefa wielofunkcyjna z zabudową mieszkaniową wielorodzinną" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="strefa wielofunkcyjna z zabudową mieszkaniową jednorodzinną" value="strefa wielofunkcyjna z zabudową mieszkaniową jednorodzinną" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="strefa wielofunkcyjna z zabudową zagrodową" value="strefa wielofunkcyjna z zabudową zagrodową" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="strefa usługowa" value="strefa usługowa" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="strefa handlu wielkopowierzchniowego" value="strefa handlu wielkopowierzchniowego" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="strefa gospodarcza" value="strefa gospodarcza" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="strefa produkcji rolniczej" value="strefa produkcji rolniczej" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="strefa infrastrukturalna" value="strefa infrastrukturalna" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="strefa zieleni i rekreacji" value="strefa zieleni i rekreacji" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="strefa cmentarzy" value="strefa cmentarzy" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="strefa górnictwa" value="strefa górnictwa" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="strefa otwarta" value="strefa otwarta" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="strefa komunikacyjna" value="strefa komunikacyjna" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="NULL" value="{2839923C-8B7D-419E-B84B-CA2FE9B80EC7}" type="QString"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="nazwaAlternatywna">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="profilPodstawowy">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="profilDodatkowy">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="maksNadziemnaIntensywnoscZabudowy">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="maksUdzialPowierzchniZabudowy">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="maksWysokoscZabudowy">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="minUdzialPowierzchniBiologicznieCzynnej">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias name="" field="fid" index="0"/>
    <alias name="" field="gml_id" index="1"/>
    <alias name="" field="przestrzenNazw" index="2"/>
    <alias name="" field="lokalnyId" index="3"/>
    <alias name="" field="wersjaId" index="4"/>
    <alias name="" field="oznaczenie" index="5"/>
    <alias name="" field="symbol" index="6"/>
    <alias name="" field="charakterUstalenia" index="7"/>
    <alias name="" field="obowiazujeOd" index="8"/>
    <alias name="" field="obowiazujeDo" index="9"/>
    <alias name="" field="status" index="10"/>
    <alias name="" field="poczatekWersjiObiektu" index="11"/>
    <alias name="" field="koniecWersjiObiektu" index="12"/>
    <alias name="" field="plan" index="13"/>
    <alias name="" field="nazwa" index="14"/>
    <alias name="" field="nazwaAlternatywna" index="15"/>
    <alias name="" field="profilPodstawowy" index="16"/>
    <alias name="" field="profilDodatkowy" index="17"/>
    <alias name="" field="maksNadziemnaIntensywnoscZabudowy" index="18"/>
    <alias name="" field="maksUdzialPowierzchniZabudowy" index="19"/>
    <alias name="" field="maksWysokoscZabudowy" index="20"/>
    <alias name="" field="minUdzialPowierzchniBiologicznieCzynnej" index="21"/>
  </aliases>
  <defaults>
    <default expression="" field="fid" applyOnUpdate="0"/>
    <default expression="" field="gml_id" applyOnUpdate="0"/>
    <default expression="" field="przestrzenNazw" applyOnUpdate="0"/>
    <default expression="" field="lokalnyId" applyOnUpdate="0"/>
    <default expression="" field="wersjaId" applyOnUpdate="0"/>
    <default expression="" field="oznaczenie" applyOnUpdate="0"/>
    <default expression="NULL" field="symbol" applyOnUpdate="0"/>
    <default expression="'ogólnie wiążące'" field="charakterUstalenia" applyOnUpdate="0"/>
    <default expression="" field="obowiazujeOd" applyOnUpdate="0"/>
    <default expression="" field="obowiazujeDo" applyOnUpdate="0"/>
    <default expression="" field="status" applyOnUpdate="0"/>
    <default expression="" field="poczatekWersjiObiektu" applyOnUpdate="0"/>
    <default expression="" field="koniecWersjiObiektu" applyOnUpdate="0"/>
    <default expression="" field="plan" applyOnUpdate="0"/>
    <default expression="NULL" field="nazwa" applyOnUpdate="0"/>
    <default expression="" field="nazwaAlternatywna" applyOnUpdate="0"/>
    <default expression="" field="profilPodstawowy" applyOnUpdate="0"/>
    <default expression="" field="profilDodatkowy" applyOnUpdate="0"/>
    <default expression="" field="maksNadziemnaIntensywnoscZabudowy" applyOnUpdate="0"/>
    <default expression="" field="maksUdzialPowierzchniZabudowy" applyOnUpdate="0"/>
    <default expression="" field="maksWysokoscZabudowy" applyOnUpdate="0"/>
    <default expression="" field="minUdzialPowierzchniBiologicznieCzynnej" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint notnull_strength="1" unique_strength="1" exp_strength="0" field="fid" constraints="3"/>
    <constraint notnull_strength="0" unique_strength="0" exp_strength="0" field="gml_id" constraints="0"/>
    <constraint notnull_strength="0" unique_strength="0" exp_strength="0" field="przestrzenNazw" constraints="0"/>
    <constraint notnull_strength="0" unique_strength="0" exp_strength="0" field="lokalnyId" constraints="0"/>
    <constraint notnull_strength="0" unique_strength="0" exp_strength="0" field="wersjaId" constraints="0"/>
    <constraint notnull_strength="0" unique_strength="0" exp_strength="0" field="oznaczenie" constraints="0"/>
    <constraint notnull_strength="0" unique_strength="0" exp_strength="0" field="symbol" constraints="0"/>
    <constraint notnull_strength="0" unique_strength="0" exp_strength="0" field="charakterUstalenia" constraints="0"/>
    <constraint notnull_strength="0" unique_strength="0" exp_strength="0" field="obowiazujeOd" constraints="0"/>
    <constraint notnull_strength="0" unique_strength="0" exp_strength="0" field="obowiazujeDo" constraints="0"/>
    <constraint notnull_strength="0" unique_strength="0" exp_strength="0" field="status" constraints="0"/>
    <constraint notnull_strength="0" unique_strength="0" exp_strength="0" field="poczatekWersjiObiektu" constraints="0"/>
    <constraint notnull_strength="0" unique_strength="0" exp_strength="0" field="koniecWersjiObiektu" constraints="0"/>
    <constraint notnull_strength="0" unique_strength="0" exp_strength="0" field="plan" constraints="0"/>
    <constraint notnull_strength="0" unique_strength="0" exp_strength="0" field="nazwa" constraints="0"/>
    <constraint notnull_strength="0" unique_strength="0" exp_strength="0" field="nazwaAlternatywna" constraints="0"/>
    <constraint notnull_strength="0" unique_strength="0" exp_strength="0" field="profilPodstawowy" constraints="0"/>
    <constraint notnull_strength="0" unique_strength="0" exp_strength="0" field="profilDodatkowy" constraints="0"/>
    <constraint notnull_strength="0" unique_strength="0" exp_strength="0" field="maksNadziemnaIntensywnoscZabudowy" constraints="0"/>
    <constraint notnull_strength="0" unique_strength="0" exp_strength="0" field="maksUdzialPowierzchniZabudowy" constraints="0"/>
    <constraint notnull_strength="0" unique_strength="0" exp_strength="0" field="maksWysokoscZabudowy" constraints="0"/>
    <constraint notnull_strength="0" unique_strength="0" exp_strength="0" field="minUdzialPowierzchniBiologicznieCzynnej" constraints="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="fid" desc="" exp=""/>
    <constraint field="gml_id" desc="" exp=""/>
    <constraint field="przestrzenNazw" desc="" exp=""/>
    <constraint field="lokalnyId" desc="" exp=""/>
    <constraint field="wersjaId" desc="" exp=""/>
    <constraint field="oznaczenie" desc="" exp=""/>
    <constraint field="symbol" desc="" exp=""/>
    <constraint field="charakterUstalenia" desc="" exp=""/>
    <constraint field="obowiazujeOd" desc="" exp=""/>
    <constraint field="obowiazujeDo" desc="" exp=""/>
    <constraint field="status" desc="" exp=""/>
    <constraint field="poczatekWersjiObiektu" desc="" exp=""/>
    <constraint field="koniecWersjiObiektu" desc="" exp=""/>
    <constraint field="plan" desc="" exp=""/>
    <constraint field="nazwa" desc="" exp=""/>
    <constraint field="nazwaAlternatywna" desc="" exp=""/>
    <constraint field="profilPodstawowy" desc="" exp=""/>
    <constraint field="profilDodatkowy" desc="" exp=""/>
    <constraint field="maksNadziemnaIntensywnoscZabudowy" desc="" exp=""/>
    <constraint field="maksUdzialPowierzchniZabudowy" desc="" exp=""/>
    <constraint field="maksWysokoscZabudowy" desc="" exp=""/>
    <constraint field="minUdzialPowierzchniBiologicznieCzynnej" desc="" exp=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig sortOrder="0" actionWidgetStyle="dropDown" sortExpression="">
    <columns>
      <column name="przestrzenNazw" type="field" width="174" hidden="0"/>
      <column name="lokalnyId" type="field" width="-1" hidden="0"/>
      <column name="wersjaId" type="field" width="-1" hidden="0"/>
      <column name="poczatekWersjiObiektu" type="field" width="-1" hidden="0"/>
      <column name="koniecWersjiObiektu" type="field" width="-1" hidden="0"/>
      <column name="obowiazujeOd" type="field" width="-1" hidden="0"/>
      <column name="obowiazujeDo" type="field" width="-1" hidden="0"/>
      <column name="oznaczenie" type="field" width="-1" hidden="0"/>
      <column name="symbol" type="field" width="-1" hidden="0"/>
      <column name="charakterUstalenia" type="field" width="-1" hidden="0"/>
      <column name="status" type="field" width="-1" hidden="0"/>
      <column name="plan" type="field" width="-1" hidden="0"/>
      <column name="nazwa" type="field" width="-1" hidden="0"/>
      <column name="nazwaAlternatywna" type="field" width="-1" hidden="0"/>
      <column name="profilPodstawowy" type="field" width="540" hidden="0"/>
      <column name="profilDodatkowy" type="field" width="-1" hidden="0"/>
      <column name="maksNadziemnaIntensywnoscZabudowy" type="field" width="-1" hidden="0"/>
      <column name="maksUdzialPowierzchniZabudowy" type="field" width="-1" hidden="0"/>
      <column name="maksWysokoscZabudowy" type="field" width="-1" hidden="0"/>
      <column name="minUdzialPowierzchniBiologicznieCzynnej" type="field" width="-1" hidden="0"/>
      <column name="fid" type="field" width="-1" hidden="0"/>
      <column name="gml_id" type="field" width="-1" hidden="0"/>
      <column type="actions" width="-1" hidden="1"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <storedexpressions/>
  <editform tolerant="1">C:\Users\mlebiecki\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\wtyczka_qgis_app\StrefaPlanistyczna.ui</editform>
  <editforminit>my_form_open</editforminit>
  <editforminitcodesource>1</editforminitcodesource>
  <editforminitfilepath>C:\Users\mlebiecki\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\wtyczka_qgis_app\StrefaPlanistyczna.py</editforminitfilepath>
  <editforminitcode><![CDATA[# -*- coding: utf-8 -*-
"""
QGIS forms can have a Python function that is called when the form is
opened.

Use this function to add extra logic to your forms.

Enter the name of the function in the "Python Init function"
field.
An example follows:
"""
from qgis.PyQt.QtWidgets import QWidget

def my_form_open(dialog, layer, feature):
    geom = feature.geometry()
    control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>uifilelayout</editorlayout>
  <editable>
    <field name="charakterUstalenia" editable="1"/>
    <field name="fid" editable="1"/>
    <field name="gml_id" editable="1"/>
    <field name="koniecWersjiObiektu" editable="1"/>
    <field name="lokalnyId" editable="1"/>
    <field name="maksNadziemnaIntensywnoscZabudowy" editable="1"/>
    <field name="maksUdzialPowierzchniZabudowy" editable="1"/>
    <field name="maksWysokoscZabudowy" editable="1"/>
    <field name="minUdzialPowierzchniBiologicznieCzynnej" editable="1"/>
    <field name="nazwa" editable="1"/>
    <field name="nazwaAlternatywna" editable="1"/>
    <field name="obowiazujeDo" editable="1"/>
    <field name="obowiazujeOd" editable="1"/>
    <field name="oznaczenie" editable="1"/>
    <field name="plan" editable="1"/>
    <field name="poczatekWersjiObiektu" editable="1"/>
    <field name="profilDodatkowy" editable="1"/>
    <field name="profilPodstawowy" editable="1"/>
    <field name="przestrzenNazw" editable="0"/>
    <field name="status" editable="1"/>
    <field name="symbol" editable="1"/>
    <field name="tytul" editable="1"/>
    <field name="wersjaId" editable="1"/>
  </editable>
  <labelOnTop>
    <field name="charakterUstalenia" labelOnTop="0"/>
    <field name="fid" labelOnTop="0"/>
    <field name="gml_id" labelOnTop="0"/>
    <field name="koniecWersjiObiektu" labelOnTop="0"/>
    <field name="lokalnyId" labelOnTop="0"/>
    <field name="maksNadziemnaIntensywnoscZabudowy" labelOnTop="0"/>
    <field name="maksUdzialPowierzchniZabudowy" labelOnTop="0"/>
    <field name="maksWysokoscZabudowy" labelOnTop="0"/>
    <field name="minUdzialPowierzchniBiologicznieCzynnej" labelOnTop="0"/>
    <field name="nazwa" labelOnTop="0"/>
    <field name="nazwaAlternatywna" labelOnTop="0"/>
    <field name="obowiazujeDo" labelOnTop="0"/>
    <field name="obowiazujeOd" labelOnTop="0"/>
    <field name="oznaczenie" labelOnTop="0"/>
    <field name="plan" labelOnTop="0"/>
    <field name="poczatekWersjiObiektu" labelOnTop="0"/>
    <field name="profilDodatkowy" labelOnTop="0"/>
    <field name="profilPodstawowy" labelOnTop="0"/>
    <field name="przestrzenNazw" labelOnTop="0"/>
    <field name="status" labelOnTop="0"/>
    <field name="symbol" labelOnTop="0"/>
    <field name="tytul" labelOnTop="0"/>
    <field name="wersjaId" labelOnTop="0"/>
  </labelOnTop>
  <reuseLastValue>
    <field name="charakterUstalenia" reuseLastValue="0"/>
    <field name="fid" reuseLastValue="0"/>
    <field name="gml_id" reuseLastValue="0"/>
    <field name="koniecWersjiObiektu" reuseLastValue="0"/>
    <field name="lokalnyId" reuseLastValue="0"/>
    <field name="maksNadziemnaIntensywnoscZabudowy" reuseLastValue="0"/>
    <field name="maksUdzialPowierzchniZabudowy" reuseLastValue="0"/>
    <field name="maksWysokoscZabudowy" reuseLastValue="0"/>
    <field name="minUdzialPowierzchniBiologicznieCzynnej" reuseLastValue="0"/>
    <field name="nazwa" reuseLastValue="0"/>
    <field name="nazwaAlternatywna" reuseLastValue="0"/>
    <field name="obowiazujeDo" reuseLastValue="0"/>
    <field name="obowiazujeOd" reuseLastValue="0"/>
    <field name="oznaczenie" reuseLastValue="0"/>
    <field name="plan" reuseLastValue="0"/>
    <field name="poczatekWersjiObiektu" reuseLastValue="0"/>
    <field name="profilDodatkowy" reuseLastValue="0"/>
    <field name="profilPodstawowy" reuseLastValue="0"/>
    <field name="przestrzenNazw" reuseLastValue="0"/>
    <field name="status" reuseLastValue="0"/>
    <field name="symbol" reuseLastValue="0"/>
    <field name="tytul" reuseLastValue="0"/>
    <field name="wersjaId" reuseLastValue="0"/>
  </reuseLastValue>
  <dataDefinedFieldProperties/>
  <widgets/>
  <mapTip></mapTip>
  <layerGeometryType>2</layerGeometryType>
</qgis>

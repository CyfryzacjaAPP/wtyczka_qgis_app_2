<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis hasScaleBasedVisibilityFlag="0" simplifyLocal="1" symbologyReferenceScale="-1" simplifyDrawingTol="2" minScale="100000000" version="3.22.15-Białowieża" labelsEnabled="1" simplifyMaxScale="1" styleCategories="Symbology|Symbology3D|Labeling|Fields|Forms|Actions|MapTips|Diagrams|AttributeTable|Rendering|CustomProperties|GeometryOptions|Relations|Temporal|Legend|Elevation|Notes" simplifyAlgorithm="0" maxScale="0" simplifyDrawingHints="0">
  <temporal startExpression="" endExpression="" startField="poczatekWersjiObiektu" mode="0" durationUnit="min" endField="" durationField="fid" fixedDuration="0" accumulate="0" enabled="0" limitMode="0">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <renderer-v2 enableorderby="0" type="singleSymbol" symbollevels="0" referencescale="-1" forceraster="0">
    <symbols>
      <symbol name="0" force_rhr="0" type="fill" clip_to_extent="1" alpha="1">
        <data_defined_properties>
          <Option type="Map">
            <Option value="" name="name" type="QString"/>
            <Option name="properties"/>
            <Option value="collection" name="type" type="QString"/>
          </Option>
        </data_defined_properties>
        <layer class="SimpleFill" pass="0" locked="0" enabled="1">
          <Option type="Map">
            <Option value="3x:0,0,0,0,0,0" name="border_width_map_unit_scale" type="QString"/>
            <Option value="189,189,189,255" name="color" type="QString"/>
            <Option value="bevel" name="joinstyle" type="QString"/>
            <Option value="0,0" name="offset" type="QString"/>
            <Option value="3x:0,0,0,0,0,0" name="offset_map_unit_scale" type="QString"/>
            <Option value="MM" name="offset_unit" type="QString"/>
            <Option value="35,35,35,255" name="outline_color" type="QString"/>
            <Option value="no" name="outline_style" type="QString"/>
            <Option value="0" name="outline_width" type="QString"/>
            <Option value="MM" name="outline_width_unit" type="QString"/>
            <Option value="solid" name="style" type="QString"/>
          </Option>
          <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="color" v="189,189,189,255"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="35,35,35,255"/>
          <prop k="outline_style" v="no"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="style" v="solid"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" name="name" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="fillColor" type="Map">
                  <Option value="true" name="active" type="bool"/>
                  <Option value="CASE&#xd;&#xa;WHEN  &quot;symbol&quot; = 'SW' THEN &#xd;&#xa;color_rgb(154,124,100)&#xd;&#xa;WHEN  &quot;symbol&quot; = 'SJ' THEN &#xd;&#xa;color_rgb(217,180,115)&#xd;&#xa;WHEN  &quot;symbol&quot; = 'SZ' THEN &#xd;&#xa;color_rgb(255,230,171)&#xd;&#xa;WHEN  &quot;symbol&quot; = 'SU' THEN &#xd;&#xa;color_rgb(255,108,105)&#xd;&#xa;WHEN  &quot;symbol&quot; = 'SH' THEN &#xd;&#xa;color_rgb(255,132,183)&#xd;&#xa;WHEN  &quot;symbol&quot; = 'SP' THEN &#xd;&#xa;color_rgb(175,136,222)&#xd;&#xa;WHEN  &quot;symbol&quot; = 'SR' THEN &#xd;&#xa;color_rgb(254,239,100)&#xd;&#xa;WHEN  &quot;symbol&quot; = 'SI' THEN&#xd;&#xa;color_rgb(204,204,204)&#xd;&#xa;WHEN  &quot;symbol&quot; = 'SN' THEN &#xd;&#xa;color_rgb(187,245,139)&#xd;&#xa;WHEN  &quot;symbol&quot; = 'SC' THEN &#xd;&#xa;color_rgb(148,212,196)&#xd;&#xa;WHEN  &quot;symbol&quot; = 'SG' THEN&#xd;&#xa;color_rgb(252,212,255)&#xd;&#xa;WHEN  &quot;symbol&quot; = 'SO' THEN &#xd;&#xa;color_rgb(227,255,199)&#xd;&#xa;WHEN  &quot;symbol&quot; = 'SK' THEN color_rgb(242,242,242)&#xd;&#xa;END" name="expression" type="QString"/>
                  <Option value="3" name="type" type="int"/>
                </Option>
              </Option>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer class="SimpleLine" pass="0" locked="0" enabled="1">
          <Option type="Map">
            <Option value="0" name="align_dash_pattern" type="QString"/>
            <Option value="square" name="capstyle" type="QString"/>
            <Option value="13.5;4.5" name="customdash" type="QString"/>
            <Option value="3x:0,0,0,0,0,0" name="customdash_map_unit_scale" type="QString"/>
            <Option value="MM" name="customdash_unit" type="QString"/>
            <Option value="0" name="dash_pattern_offset" type="QString"/>
            <Option value="3x:0,0,0,0,0,0" name="dash_pattern_offset_map_unit_scale" type="QString"/>
            <Option value="MM" name="dash_pattern_offset_unit" type="QString"/>
            <Option value="0" name="draw_inside_polygon" type="QString"/>
            <Option value="miter" name="joinstyle" type="QString"/>
            <Option value="83,83,83,255" name="line_color" type="QString"/>
            <Option value="solid" name="line_style" type="QString"/>
            <Option value="0.5" name="line_width" type="QString"/>
            <Option value="MM" name="line_width_unit" type="QString"/>
            <Option value="0" name="offset" type="QString"/>
            <Option value="3x:0,0,0,0,0,0" name="offset_map_unit_scale" type="QString"/>
            <Option value="MM" name="offset_unit" type="QString"/>
            <Option value="0" name="ring_filter" type="QString"/>
            <Option value="0" name="trim_distance_end" type="QString"/>
            <Option value="3x:0,0,0,0,0,0" name="trim_distance_end_map_unit_scale" type="QString"/>
            <Option value="MM" name="trim_distance_end_unit" type="QString"/>
            <Option value="0" name="trim_distance_start" type="QString"/>
            <Option value="3x:0,0,0,0,0,0" name="trim_distance_start_map_unit_scale" type="QString"/>
            <Option value="MM" name="trim_distance_start_unit" type="QString"/>
            <Option value="0" name="tweak_dash_pattern_on_corners" type="QString"/>
            <Option value="0" name="use_custom_dash" type="QString"/>
            <Option value="3x:0,0,0,0,0,0" name="width_map_unit_scale" type="QString"/>
          </Option>
          <prop k="align_dash_pattern" v="0"/>
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="13.5;4.5"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="dash_pattern_offset" v="0"/>
          <prop k="dash_pattern_offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="dash_pattern_offset_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="miter"/>
          <prop k="line_color" v="83,83,83,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="0.5"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="trim_distance_end" v="0"/>
          <prop k="trim_distance_end_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="trim_distance_end_unit" v="MM"/>
          <prop k="trim_distance_start" v="0"/>
          <prop k="trim_distance_start_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="trim_distance_start_unit" v="MM"/>
          <prop k="tweak_dash_pattern_on_corners" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" name="name" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="outlineWidth" type="Map">
                  <Option value="true" name="active" type="bool"/>
                  <Option value="if(@map_scale&lt;=10000,0.5,0.25)" name="expression" type="QString"/>
                  <Option value="3" name="type" type="int"/>
                </Option>
              </Option>
              <Option value="collection" name="type" type="QString"/>
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
      <text-style fontLetterSpacing="0" isExpression="0" fontItalic="0" namedStyle="Normal" textColor="0,0,0,255" blendMode="0" capitalization="0" textOpacity="1" fontWeight="50" useSubstitutions="0" fontStrikeout="0" allowHtml="0" previewBkgrdColor="255,255,255,255" fontFamily="Arial" textOrientation="horizontal" fontKerning="1" legendString="Aa" fontSizeUnit="MM" multilineHeight="1" fontSizeMapUnitScale="3x:0,0,0,0,0,0" fieldName="oznaczenie" fontWordSpacing="0" fontUnderline="0" fontSize="3">
        <families/>
        <text-buffer bufferBlendMode="0" bufferSizeUnits="MM" bufferColor="255,255,255,255" bufferSize="0.5" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferOpacity="1" bufferJoinStyle="128" bufferNoFill="1" bufferDraw="1"/>
        <text-mask maskSizeMapUnitScale="3x:0,0,0,0,0,0" maskSize="0" maskJoinStyle="128" maskedSymbolLayers="" maskOpacity="1" maskSizeUnits="MM" maskType="0" maskEnabled="0"/>
        <background shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeDraw="0" shapeBorderWidthUnit="Point" shapeBlendMode="0" shapeSizeY="0" shapeOffsetX="0" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeOffsetY="0" shapeSizeX="0" shapeRotation="0" shapeOpacity="1" shapeSizeType="0" shapeRadiiUnit="Point" shapeOffsetUnit="Point" shapeBorderWidth="0" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeType="0" shapeJoinStyle="64" shapeRotationType="0" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeRadiiY="0" shapeSizeUnit="Point" shapeRadiiX="0" shapeBorderColor="128,128,128,255" shapeFillColor="255,255,255,255" shapeSVGFile="">
          <symbol name="markerSymbol" force_rhr="0" type="marker" clip_to_extent="1" alpha="1">
            <data_defined_properties>
              <Option type="Map">
                <Option value="" name="name" type="QString"/>
                <Option name="properties"/>
                <Option value="collection" name="type" type="QString"/>
              </Option>
            </data_defined_properties>
            <layer class="SimpleMarker" pass="0" locked="0" enabled="1">
              <Option type="Map">
                <Option value="0" name="angle" type="QString"/>
                <Option value="square" name="cap_style" type="QString"/>
                <Option value="183,72,75,255" name="color" type="QString"/>
                <Option value="1" name="horizontal_anchor_point" type="QString"/>
                <Option value="bevel" name="joinstyle" type="QString"/>
                <Option value="circle" name="name" type="QString"/>
                <Option value="0,0" name="offset" type="QString"/>
                <Option value="3x:0,0,0,0,0,0" name="offset_map_unit_scale" type="QString"/>
                <Option value="MM" name="offset_unit" type="QString"/>
                <Option value="35,35,35,255" name="outline_color" type="QString"/>
                <Option value="solid" name="outline_style" type="QString"/>
                <Option value="0" name="outline_width" type="QString"/>
                <Option value="3x:0,0,0,0,0,0" name="outline_width_map_unit_scale" type="QString"/>
                <Option value="MM" name="outline_width_unit" type="QString"/>
                <Option value="diameter" name="scale_method" type="QString"/>
                <Option value="2" name="size" type="QString"/>
                <Option value="3x:0,0,0,0,0,0" name="size_map_unit_scale" type="QString"/>
                <Option value="MM" name="size_unit" type="QString"/>
                <Option value="1" name="vertical_anchor_point" type="QString"/>
              </Option>
              <prop k="angle" v="0"/>
              <prop k="cap_style" v="square"/>
              <prop k="color" v="183,72,75,255"/>
              <prop k="horizontal_anchor_point" v="1"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="name" v="circle"/>
              <prop k="offset" v="0,0"/>
              <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="outline_color" v="35,35,35,255"/>
              <prop k="outline_style" v="solid"/>
              <prop k="outline_width" v="0"/>
              <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="outline_width_unit" v="MM"/>
              <prop k="scale_method" v="diameter"/>
              <prop k="size" v="2"/>
              <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="size_unit" v="MM"/>
              <prop k="vertical_anchor_point" v="1"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option value="" name="name" type="QString"/>
                  <Option name="properties"/>
                  <Option value="collection" name="type" type="QString"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
          <symbol name="fillSymbol" force_rhr="0" type="fill" clip_to_extent="1" alpha="1">
            <data_defined_properties>
              <Option type="Map">
                <Option value="" name="name" type="QString"/>
                <Option name="properties"/>
                <Option value="collection" name="type" type="QString"/>
              </Option>
            </data_defined_properties>
            <layer class="SimpleFill" pass="0" locked="0" enabled="1">
              <Option type="Map">
                <Option value="3x:0,0,0,0,0,0" name="border_width_map_unit_scale" type="QString"/>
                <Option value="255,255,255,255" name="color" type="QString"/>
                <Option value="bevel" name="joinstyle" type="QString"/>
                <Option value="0,0" name="offset" type="QString"/>
                <Option value="3x:0,0,0,0,0,0" name="offset_map_unit_scale" type="QString"/>
                <Option value="MM" name="offset_unit" type="QString"/>
                <Option value="128,128,128,255" name="outline_color" type="QString"/>
                <Option value="no" name="outline_style" type="QString"/>
                <Option value="0" name="outline_width" type="QString"/>
                <Option value="Point" name="outline_width_unit" type="QString"/>
                <Option value="solid" name="style" type="QString"/>
              </Option>
              <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="color" v="255,255,255,255"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="offset" v="0,0"/>
              <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="outline_color" v="128,128,128,255"/>
              <prop k="outline_style" v="no"/>
              <prop k="outline_width" v="0"/>
              <prop k="outline_width_unit" v="Point"/>
              <prop k="style" v="solid"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option value="" name="name" type="QString"/>
                  <Option name="properties"/>
                  <Option value="collection" name="type" type="QString"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </background>
        <shadow shadowUnder="0" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowScale="100" shadowOffsetGlobal="1" shadowBlendMode="6" shadowRadiusUnit="MM" shadowOffsetUnit="MM" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowRadiusAlphaOnly="0" shadowRadius="1.5" shadowDraw="0" shadowOffsetDist="1" shadowOffsetAngle="135" shadowOpacity="0.69999999999999996" shadowColor="0,0,0,255"/>
        <dd_properties>
          <Option type="Map">
            <Option value="" name="name" type="QString"/>
            <Option name="properties"/>
            <Option value="collection" name="type" type="QString"/>
          </Option>
        </dd_properties>
        <substitutions/>
      </text-style>
      <text-format useMaxLineLengthForAutoWrap="1" plussign="0" autoWrapLength="0" multilineAlign="3" formatNumbers="0" decimals="3" rightDirectionSymbol=">" addDirectionSymbol="0" wrapChar="" leftDirectionSymbol="&lt;" placeDirectionSymbol="0" reverseDirectionSymbol="0"/>
      <placement preserveRotation="1" geometryGeneratorType="PointGeometry" dist="0" maxCurvedCharAngleOut="-25" repeatDistanceUnits="MM" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" geometryGeneratorEnabled="0" geometryGenerator="" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" distUnits="MM" placement="0" lineAnchorType="0" rotationUnit="AngleDegrees" centroidInside="1" distMapUnitScale="3x:0,0,0,0,0,0" polygonPlacementFlags="2" layerType="PolygonGeometry" maxCurvedCharAngleIn="25" priority="10" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" xOffset="0" centroidWhole="0" lineAnchorClipping="0" fitInPolygonOnly="0" repeatDistance="0" offsetType="0" quadOffset="4" yOffset="0" rotationAngle="0" placementFlags="10" offsetUnits="MM" overrunDistance="0" lineAnchorPercent="0.5" overrunDistanceUnit="MM"/>
      <rendering obstacle="1" limitNumLabels="0" zIndex="0" minFeatureSize="0" scaleMin="0" obstacleType="1" upsidedownLabels="0" displayAll="0" labelPerPart="0" fontLimitPixelSize="0" scaleVisibility="0" scaleMax="0" drawLabels="1" fontMinPixelSize="3" unplacedVisibility="0" maxNumLabels="2000" mergeLines="0" fontMaxPixelSize="10000" obstacleFactor="1"/>
      <dd_properties>
        <Option type="Map">
          <Option value="" name="name" type="QString"/>
          <Option name="properties" type="Map">
            <Option name="Size" type="Map">
              <Option value="true" name="active" type="bool"/>
              <Option value="if(@map_scale&lt;=10000,3,0)" name="expression" type="QString"/>
              <Option value="3" name="type" type="int"/>
            </Option>
          </Option>
          <Option value="collection" name="type" type="QString"/>
        </Option>
      </dd_properties>
      <callout type="simple">
        <Option type="Map">
          <Option value="pole_of_inaccessibility" name="anchorPoint" type="QString"/>
          <Option value="0" name="blendMode" type="int"/>
          <Option name="ddProperties" type="Map">
            <Option value="" name="name" type="QString"/>
            <Option name="properties"/>
            <Option value="collection" name="type" type="QString"/>
          </Option>
          <Option value="false" name="drawToAllParts" type="bool"/>
          <Option value="0" name="enabled" type="QString"/>
          <Option value="point_on_exterior" name="labelAnchorPoint" type="QString"/>
          <Option value="&lt;symbol name=&quot;symbol&quot; force_rhr=&quot;0&quot; type=&quot;line&quot; clip_to_extent=&quot;1&quot; alpha=&quot;1&quot;>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option value=&quot;&quot; name=&quot;name&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option value=&quot;collection&quot; name=&quot;type&quot; type=&quot;QString&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;layer class=&quot;SimpleLine&quot; pass=&quot;0&quot; locked=&quot;0&quot; enabled=&quot;1&quot;>&lt;Option type=&quot;Map&quot;>&lt;Option value=&quot;0&quot; name=&quot;align_dash_pattern&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;square&quot; name=&quot;capstyle&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;5;2&quot; name=&quot;customdash&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; name=&quot;customdash_map_unit_scale&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;MM&quot; name=&quot;customdash_unit&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;0&quot; name=&quot;dash_pattern_offset&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; name=&quot;dash_pattern_offset_map_unit_scale&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;MM&quot; name=&quot;dash_pattern_offset_unit&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;0&quot; name=&quot;draw_inside_polygon&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;bevel&quot; name=&quot;joinstyle&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;60,60,60,255&quot; name=&quot;line_color&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;solid&quot; name=&quot;line_style&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;0.3&quot; name=&quot;line_width&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;MM&quot; name=&quot;line_width_unit&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;0&quot; name=&quot;offset&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; name=&quot;offset_map_unit_scale&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;MM&quot; name=&quot;offset_unit&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;0&quot; name=&quot;ring_filter&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;0&quot; name=&quot;trim_distance_end&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; name=&quot;trim_distance_end_map_unit_scale&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;MM&quot; name=&quot;trim_distance_end_unit&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;0&quot; name=&quot;trim_distance_start&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; name=&quot;trim_distance_start_map_unit_scale&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;MM&quot; name=&quot;trim_distance_start_unit&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;0&quot; name=&quot;tweak_dash_pattern_on_corners&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;0&quot; name=&quot;use_custom_dash&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; name=&quot;width_map_unit_scale&quot; type=&quot;QString&quot;/>&lt;/Option>&lt;prop k=&quot;align_dash_pattern&quot; v=&quot;0&quot;/>&lt;prop k=&quot;capstyle&quot; v=&quot;square&quot;/>&lt;prop k=&quot;customdash&quot; v=&quot;5;2&quot;/>&lt;prop k=&quot;customdash_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;customdash_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;dash_pattern_offset&quot; v=&quot;0&quot;/>&lt;prop k=&quot;dash_pattern_offset_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;dash_pattern_offset_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;draw_inside_polygon&quot; v=&quot;0&quot;/>&lt;prop k=&quot;joinstyle&quot; v=&quot;bevel&quot;/>&lt;prop k=&quot;line_color&quot; v=&quot;60,60,60,255&quot;/>&lt;prop k=&quot;line_style&quot; v=&quot;solid&quot;/>&lt;prop k=&quot;line_width&quot; v=&quot;0.3&quot;/>&lt;prop k=&quot;line_width_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;offset&quot; v=&quot;0&quot;/>&lt;prop k=&quot;offset_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;offset_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;ring_filter&quot; v=&quot;0&quot;/>&lt;prop k=&quot;trim_distance_end&quot; v=&quot;0&quot;/>&lt;prop k=&quot;trim_distance_end_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;trim_distance_end_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;trim_distance_start&quot; v=&quot;0&quot;/>&lt;prop k=&quot;trim_distance_start_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;trim_distance_start_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;tweak_dash_pattern_on_corners&quot; v=&quot;0&quot;/>&lt;prop k=&quot;use_custom_dash&quot; v=&quot;0&quot;/>&lt;prop k=&quot;width_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option value=&quot;&quot; name=&quot;name&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option value=&quot;collection&quot; name=&quot;type&quot; type=&quot;QString&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>" name="lineSymbol" type="QString"/>
          <Option value="0" name="minLength" type="double"/>
          <Option value="3x:0,0,0,0,0,0" name="minLengthMapUnitScale" type="QString"/>
          <Option value="MM" name="minLengthUnit" type="QString"/>
          <Option value="0" name="offsetFromAnchor" type="double"/>
          <Option value="3x:0,0,0,0,0,0" name="offsetFromAnchorMapUnitScale" type="QString"/>
          <Option value="MM" name="offsetFromAnchorUnit" type="QString"/>
          <Option value="0" name="offsetFromLabel" type="double"/>
          <Option value="3x:0,0,0,0,0,0" name="offsetFromLabelMapUnitScale" type="QString"/>
          <Option value="MM" name="offsetFromLabelUnit" type="QString"/>
        </Option>
      </callout>
    </settings>
  </labeling>
  <customproperties>
    <Option type="Map">
      <Option name="dualview/previewExpressions" type="List">
        <Option value="&quot;przestrzenNazw&quot;" type="QString"/>
        <Option value="&quot;gml_id&quot;" type="QString"/>
      </Option>
      <Option value="0" name="embeddedWidgets/count" type="int"/>
      <Option name="variableNames"/>
      <Option name="variableValues"/>
    </Option>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer diagramType="Histogram" attributeLegend="1">
    <DiagramCategory diagramOrientation="Up" rotationOffset="270" spacingUnit="MM" enabled="0" barWidth="5" backgroundAlpha="255" width="15" maxScaleDenominator="1e+08" showAxis="1" penWidth="0" penColor="#000000" lineSizeType="MM" sizeScale="3x:0,0,0,0,0,0" penAlpha="255" backgroundColor="#ffffff" opacity="1" height="15" spacing="5" spacingUnitScale="3x:0,0,0,0,0,0" direction="0" scaleDependency="Area" scaleBasedVisibility="0" minimumSize="0" sizeType="MM" labelPlacementMethod="XHeight" minScaleDenominator="0" lineSizeScale="3x:0,0,0,0,0,0">
      <fontProperties style="" description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0"/>
      <attribute field="" colorOpacity="1" label="" color="#000000"/>
      <axisSymbol>
        <symbol name="" force_rhr="0" type="line" clip_to_extent="1" alpha="1">
          <data_defined_properties>
            <Option type="Map">
              <Option value="" name="name" type="QString"/>
              <Option name="properties"/>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
          <layer class="SimpleLine" pass="0" locked="0" enabled="1">
            <Option type="Map">
              <Option value="0" name="align_dash_pattern" type="QString"/>
              <Option value="square" name="capstyle" type="QString"/>
              <Option value="5;2" name="customdash" type="QString"/>
              <Option value="3x:0,0,0,0,0,0" name="customdash_map_unit_scale" type="QString"/>
              <Option value="MM" name="customdash_unit" type="QString"/>
              <Option value="0" name="dash_pattern_offset" type="QString"/>
              <Option value="3x:0,0,0,0,0,0" name="dash_pattern_offset_map_unit_scale" type="QString"/>
              <Option value="MM" name="dash_pattern_offset_unit" type="QString"/>
              <Option value="0" name="draw_inside_polygon" type="QString"/>
              <Option value="bevel" name="joinstyle" type="QString"/>
              <Option value="35,35,35,255" name="line_color" type="QString"/>
              <Option value="solid" name="line_style" type="QString"/>
              <Option value="0.26" name="line_width" type="QString"/>
              <Option value="MM" name="line_width_unit" type="QString"/>
              <Option value="0" name="offset" type="QString"/>
              <Option value="3x:0,0,0,0,0,0" name="offset_map_unit_scale" type="QString"/>
              <Option value="MM" name="offset_unit" type="QString"/>
              <Option value="0" name="ring_filter" type="QString"/>
              <Option value="0" name="trim_distance_end" type="QString"/>
              <Option value="3x:0,0,0,0,0,0" name="trim_distance_end_map_unit_scale" type="QString"/>
              <Option value="MM" name="trim_distance_end_unit" type="QString"/>
              <Option value="0" name="trim_distance_start" type="QString"/>
              <Option value="3x:0,0,0,0,0,0" name="trim_distance_start_map_unit_scale" type="QString"/>
              <Option value="MM" name="trim_distance_start_unit" type="QString"/>
              <Option value="0" name="tweak_dash_pattern_on_corners" type="QString"/>
              <Option value="0" name="use_custom_dash" type="QString"/>
              <Option value="3x:0,0,0,0,0,0" name="width_map_unit_scale" type="QString"/>
            </Option>
            <prop k="align_dash_pattern" v="0"/>
            <prop k="capstyle" v="square"/>
            <prop k="customdash" v="5;2"/>
            <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
            <prop k="customdash_unit" v="MM"/>
            <prop k="dash_pattern_offset" v="0"/>
            <prop k="dash_pattern_offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
            <prop k="dash_pattern_offset_unit" v="MM"/>
            <prop k="draw_inside_polygon" v="0"/>
            <prop k="joinstyle" v="bevel"/>
            <prop k="line_color" v="35,35,35,255"/>
            <prop k="line_style" v="solid"/>
            <prop k="line_width" v="0.26"/>
            <prop k="line_width_unit" v="MM"/>
            <prop k="offset" v="0"/>
            <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
            <prop k="offset_unit" v="MM"/>
            <prop k="ring_filter" v="0"/>
            <prop k="trim_distance_end" v="0"/>
            <prop k="trim_distance_end_map_unit_scale" v="3x:0,0,0,0,0,0"/>
            <prop k="trim_distance_end_unit" v="MM"/>
            <prop k="trim_distance_start" v="0"/>
            <prop k="trim_distance_start_map_unit_scale" v="3x:0,0,0,0,0,0"/>
            <prop k="trim_distance_start_unit" v="MM"/>
            <prop k="tweak_dash_pattern_on_corners" v="0"/>
            <prop k="use_custom_dash" v="0"/>
            <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
            <data_defined_properties>
              <Option type="Map">
                <Option value="" name="name" type="QString"/>
                <Option name="properties"/>
                <Option value="collection" name="type" type="QString"/>
              </Option>
            </data_defined_properties>
          </layer>
        </symbol>
      </axisSymbol>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings obstacle="0" priority="0" showAll="1" placement="1" dist="0" zIndex="0" linePlacementFlags="18">
    <properties>
      <Option type="Map">
        <Option value="" name="name" type="QString"/>
        <Option name="properties"/>
        <Option value="collection" name="type" type="QString"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions removeDuplicateNodes="0">
    <activeChecks/>
    <checkConfiguration type="Map">
      <Option name="QgsGeometryGapCheck" type="Map">
        <Option value="0" name="allowedGapsBuffer" type="double"/>
        <Option value="false" name="allowedGapsEnabled" type="bool"/>
        <Option value="" name="allowedGapsLayer" type="QString"/>
      </Option>
    </checkConfiguration>
  </geometryOptions>
  <legend type="default-vector" showLabelLegend="0"/>
  <referencedLayers/>
  <fieldConfiguration>
    <field name="fid" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="przestrzenNazw" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="lokalnyId" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="wersjaId" configurationFlags="None">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option value="true" name="allow_null" type="bool"/>
            <Option value="true" name="calendar_popup" type="bool"/>
            <Option value="yyyyMMddTHHmmss" name="display_format" type="QString"/>
            <Option value="yyyyMMddTHHmmss" name="field_format" type="QString"/>
            <Option value="false" name="field_iso_format" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="oznaczenie" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="symbol" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option value="SW" name="SW" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="SJ" name="SJ" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="SZ" name="SZ" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="SU" name="SU" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="SH" name="SH" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="SP" name="SP" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="SR" name="SR" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="SI" name="SI" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="SN" name="SN" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="SC" name="SC" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="SG" name="SG" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="SO" name="SO" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="SK" name="SK" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="{2839923C-8B7D-419E-B84B-CA2FE9B80EC7}" name="wybierz" type="QString"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="poczatekWersjiObiektu" configurationFlags="None">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option value="true" name="allow_null" type="bool"/>
            <Option value="true" name="calendar_popup" type="bool"/>
            <Option value="yyyy-MM-ddTHH:mm:ssZ" name="display_format" type="QString"/>
            <Option value="yyyy-MM-ddTHH:mm:ssZ" name="field_format" type="QString"/>
            <Option value="false" name="field_iso_format" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="koniecWersjiObiektu" configurationFlags="None">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option value="true" name="allow_null" type="bool"/>
            <Option value="true" name="calendar_popup" type="bool"/>
            <Option value="yyyy-MM-ddTHH:mm:ssZ" name="display_format" type="QString"/>
            <Option value="yyyy-MM-ddTHH:mm:ssZ" name="field_format" type="QString"/>
            <Option value="false" name="field_iso_format" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="obowiazujeOd" configurationFlags="None">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option value="true" name="allow_null" type="bool"/>
            <Option value="true" name="calendar_popup" type="bool"/>
            <Option value="yyyy-MM-dd" name="display_format" type="QString"/>
            <Option value="yyyy-MM-dd" name="field_format" type="QString"/>
            <Option value="false" name="field_iso_format" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="obowiazujeDo" configurationFlags="None">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option value="true" name="allow_null" type="bool"/>
            <Option value="true" name="calendar_popup" type="bool"/>
            <Option value="yyyy-MM-dd" name="display_format" type="QString"/>
            <Option value="yyyy-MM-dd" name="field_format" type="QString"/>
            <Option value="false" name="field_iso_format" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="status" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option value="nieaktualny" name="nieaktualny" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="prawnie wiążący lub realizowany" name="prawnie wiążący lub realizowany" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="w opracowaniu" name="w opracowaniu" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="w trakcie przyjmowania" name="w trakcie przyjmowania" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="{2839923C-8B7D-419E-B84B-CA2FE9B80EC7}" name="wybierz" type="QString"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="charakterUstalenia" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option value="ogólnie wiążące" name="ogólnie wiążące" type="QString"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="plan" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="nazwa" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option value="strefa wielofunkcyjna z zabudową mieszkaniową wielorodzinną" name="strefa wielofunkcyjna z zabudową mieszkaniową wielorodzinną" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="strefa wielofunkcyjna z zabudową mieszkaniową jednorodzinną" name="strefa wielofunkcyjna z zabudową mieszkaniową jednorodzinną" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="strefa wielofunkcyjna z zabudową zagrodową" name="strefa wielofunkcyjna z zabudową zagrodową" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="strefa usługowa" name="strefa usługowa" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="strefa handlu wielkopowierzchniowego" name="strefa handlu wielkopowierzchniowego" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="strefa gospodarcza" name="strefa gospodarcza" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="strefa produkcji rolniczej" name="strefa produkcji rolniczej" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="strefa infrastrukturalna" name="strefa infrastrukturalna" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="strefa zieleni i rekreacji" name="strefa zieleni i rekreacji" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="strefa cmentarzy" name="strefa cmentarzy" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="strefa górnictwa" name="strefa górnictwa" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="strefa otwarta" name="strefa otwarta" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="strefa komunikacyjna" name="strefa komunikacyjna" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="{2839923C-8B7D-419E-B84B-CA2FE9B80EC7}" name="wybierz" type="QString"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="nazwaAlternatywna" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="maksNadziemnaIntensywnoscZabudowy" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="maksUdzialPowierzchniZabudowy" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="maksWysokoscZabudowy" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="minUdzialPowierzchniBiologicznieCzynnej" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="profilPodstawowy" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="profilDodatkowy" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias index="0" name="" field="fid"/>
    <alias index="1" name="" field="przestrzenNazw"/>
    <alias index="2" name="" field="lokalnyId"/>
    <alias index="3" name="" field="wersjaId"/>
    <alias index="4" name="" field="oznaczenie"/>
    <alias index="5" name="" field="symbol"/>
    <alias index="6" name="" field="poczatekWersjiObiektu"/>
    <alias index="7" name="" field="koniecWersjiObiektu"/>
    <alias index="8" name="" field="obowiazujeOd"/>
    <alias index="9" name="" field="obowiazujeDo"/>
    <alias index="10" name="" field="status"/>
    <alias index="11" name="" field="charakterUstalenia"/>
    <alias index="12" name="" field="plan"/>
    <alias index="13" name="" field="nazwa"/>
    <alias index="14" name="" field="nazwaAlternatywna"/>
    <alias index="15" name="" field="maksNadziemnaIntensywnoscZabudowy"/>
    <alias index="16" name="" field="maksUdzialPowierzchniZabudowy"/>
    <alias index="17" name="" field="maksWysokoscZabudowy"/>
    <alias index="18" name="" field="minUdzialPowierzchniBiologicznieCzynnej"/>
    <alias index="19" name="" field="profilPodstawowy"/>
    <alias index="20" name="" field="profilDodatkowy"/>
  </aliases>
  <defaults>
    <default expression="" field="fid" applyOnUpdate="0"/>
    <default expression="" field="przestrzenNazw" applyOnUpdate="0"/>
    <default expression="" field="lokalnyId" applyOnUpdate="0"/>
    <default expression="" field="wersjaId" applyOnUpdate="0"/>
    <default expression="" field="oznaczenie" applyOnUpdate="0"/>
    <default expression="wybierz" field="symbol" applyOnUpdate="0"/>
    <default expression="" field="poczatekWersjiObiektu" applyOnUpdate="0"/>
    <default expression="" field="koniecWersjiObiektu" applyOnUpdate="0"/>
    <default expression="" field="obowiazujeOd" applyOnUpdate="0"/>
    <default expression="" field="obowiazujeDo" applyOnUpdate="0"/>
    <default expression="" field="status" applyOnUpdate="0"/>
    <default expression="'ogólnie wiążące'" field="charakterUstalenia" applyOnUpdate="0"/>
    <default expression="" field="plan" applyOnUpdate="0"/>
    <default expression="NULL" field="nazwa" applyOnUpdate="0"/>
    <default expression="" field="nazwaAlternatywna" applyOnUpdate="0"/>
    <default expression="" field="maksNadziemnaIntensywnoscZabudowy" applyOnUpdate="0"/>
    <default expression="" field="maksUdzialPowierzchniZabudowy" applyOnUpdate="0"/>
    <default expression="" field="maksWysokoscZabudowy" applyOnUpdate="0"/>
    <default expression="" field="minUdzialPowierzchniBiologicznieCzynnej" applyOnUpdate="0"/>
    <default expression="" field="profilPodstawowy" applyOnUpdate="0"/>
    <default expression="" field="profilDodatkowy" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint notnull_strength="1" exp_strength="0" field="fid" constraints="3" unique_strength="1"/>
    <constraint notnull_strength="0" exp_strength="0" field="przestrzenNazw" constraints="0" unique_strength="0"/>
    <constraint notnull_strength="0" exp_strength="0" field="lokalnyId" constraints="0" unique_strength="0"/>
    <constraint notnull_strength="0" exp_strength="0" field="wersjaId" constraints="0" unique_strength="0"/>
    <constraint notnull_strength="0" exp_strength="0" field="oznaczenie" constraints="0" unique_strength="0"/>
    <constraint notnull_strength="0" exp_strength="0" field="symbol" constraints="0" unique_strength="0"/>
    <constraint notnull_strength="0" exp_strength="0" field="poczatekWersjiObiektu" constraints="0" unique_strength="0"/>
    <constraint notnull_strength="0" exp_strength="0" field="koniecWersjiObiektu" constraints="0" unique_strength="0"/>
    <constraint notnull_strength="0" exp_strength="0" field="obowiazujeOd" constraints="0" unique_strength="0"/>
    <constraint notnull_strength="0" exp_strength="0" field="obowiazujeDo" constraints="0" unique_strength="0"/>
    <constraint notnull_strength="0" exp_strength="0" field="status" constraints="0" unique_strength="0"/>
    <constraint notnull_strength="0" exp_strength="0" field="charakterUstalenia" constraints="0" unique_strength="0"/>
    <constraint notnull_strength="0" exp_strength="0" field="plan" constraints="0" unique_strength="0"/>
    <constraint notnull_strength="0" exp_strength="0" field="nazwa" constraints="0" unique_strength="0"/>
    <constraint notnull_strength="0" exp_strength="0" field="nazwaAlternatywna" constraints="0" unique_strength="0"/>
    <constraint notnull_strength="0" exp_strength="0" field="maksNadziemnaIntensywnoscZabudowy" constraints="0" unique_strength="0"/>
    <constraint notnull_strength="0" exp_strength="0" field="maksUdzialPowierzchniZabudowy" constraints="0" unique_strength="0"/>
    <constraint notnull_strength="0" exp_strength="0" field="maksWysokoscZabudowy" constraints="0" unique_strength="0"/>
    <constraint notnull_strength="0" exp_strength="0" field="minUdzialPowierzchniBiologicznieCzynnej" constraints="0" unique_strength="0"/>
    <constraint notnull_strength="0" exp_strength="0" field="profilPodstawowy" constraints="0" unique_strength="0"/>
    <constraint notnull_strength="0" exp_strength="0" field="profilDodatkowy" constraints="0" unique_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" desc="" field="fid"/>
    <constraint exp="" desc="" field="przestrzenNazw"/>
    <constraint exp="" desc="" field="lokalnyId"/>
    <constraint exp="" desc="" field="wersjaId"/>
    <constraint exp="" desc="" field="oznaczenie"/>
    <constraint exp="" desc="" field="symbol"/>
    <constraint exp="" desc="" field="poczatekWersjiObiektu"/>
    <constraint exp="" desc="" field="koniecWersjiObiektu"/>
    <constraint exp="" desc="" field="obowiazujeOd"/>
    <constraint exp="" desc="" field="obowiazujeDo"/>
    <constraint exp="" desc="" field="status"/>
    <constraint exp="" desc="" field="charakterUstalenia"/>
    <constraint exp="" desc="" field="plan"/>
    <constraint exp="" desc="" field="nazwa"/>
    <constraint exp="" desc="" field="nazwaAlternatywna"/>
    <constraint exp="" desc="" field="profilPodstawowy"/>
    <constraint exp="" desc="" field="profilDodatkowy"/>
    <constraint exp="" desc="" field="maksNadziemnaIntensywnoscZabudowy"/>
    <constraint exp="" desc="" field="maksUdzialPowierzchniZabudowy"/>
    <constraint exp="" desc="" field="maksWysokoscZabudowy"/>
    <constraint exp="" desc="" field="minUdzialPowierzchniBiologicznieCzynnej"/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig actionWidgetStyle="dropDown" sortOrder="0" sortExpression="">
    <columns>
      <column name="fid" hidden="0" width="-1" type="field"/>
      <column name="przestrzenNazw" hidden="0" width="174" type="field"/>
      <column name="lokalnyId" hidden="0" width="-1" type="field"/>
      <column name="wersjaId" hidden="0" width="-1" type="field"/>
      <column name="oznaczenie" hidden="0" width="-1" type="field"/>
      <column name="symbol" hidden="0" width="-1" type="field"/>
      <column name="poczatekWersjiObiektu" hidden="0" width="-1" type="field"/>
      <column name="koniecWersjiObiektu" hidden="0" width="-1" type="field"/>
      <column name="obowiazujeOd" hidden="0" width="-1" type="field"/>
      <column name="obowiazujeDo" hidden="0" width="-1" type="field"/>
      <column name="status" hidden="0" width="-1" type="field"/>
      <column name="charakterUstalenia" hidden="0" width="-1" type="field"/>
      <column name="plan" hidden="0" width="-1" type="field"/>
      <column name="nazwa" hidden="0" width="-1" type="field"/>
      <column name="nazwaAlternatywna" hidden="0" width="-1" type="field"/>
      <column name="profilPodstawowy" hidden="0" width="540" type="field"/>
      <column name="profilDodatkowy" hidden="0" width="-1" type="field"/>
      <column name="maksNadziemnaIntensywnoscZabudowy" hidden="0" width="-1" type="field"/>
      <column name="maksUdzialPowierzchniZabudowy" hidden="0" width="-1" type="field"/>
      <column name="maksWysokoscZabudowy" hidden="0" width="-1" type="field"/>
      <column name="minUdzialPowierzchniBiologicznieCzynnej" hidden="0" width="-1" type="field"/>
      <column hidden="1" width="-1" type="actions"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <storedexpressions/>
  <editforminit>my_form_open</editforminit>
  <editforminitcodesource>1</editforminitcodesource>
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
    <field name="przestrzenNazw" editable="1"/>
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

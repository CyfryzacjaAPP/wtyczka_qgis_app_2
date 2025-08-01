<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis simplifyDrawingHints="0" version="3.22.15-Białowieża" symbologyReferenceScale="-1" maxScale="0" simplifyDrawingTol="2" simplifyLocal="1" styleCategories="Symbology|Symbology3D|Labeling|Fields|Forms|Actions|MapTips|Diagrams|AttributeTable|Rendering|CustomProperties|GeometryOptions|Relations|Temporal|Legend|Elevation|Notes" minScale="100000000" simplifyAlgorithm="0" simplifyMaxScale="1" labelsEnabled="1" hasScaleBasedVisibilityFlag="0">
  <temporal endField="" durationUnit="min" enabled="0" mode="0" fixedDuration="0" limitMode="0" startField="" accumulate="0" durationField="fid" startExpression="" endExpression="">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <renderer-v2 symbollevels="0" forceraster="0" enableorderby="0" type="singleSymbol" referencescale="-1">
    <symbols>
      <symbol force_rhr="0" alpha="1" clip_to_extent="1" name="0" type="fill">
        <data_defined_properties>
          <Option type="Map">
            <Option name="name" value="" type="QString"/>
            <Option name="properties"/>
            <Option name="type" value="collection" type="QString"/>
          </Option>
        </data_defined_properties>
        <layer locked="0" class="SimpleLine" enabled="1" pass="0">
          <Option type="Map">
            <Option name="align_dash_pattern" value="0" type="QString"/>
            <Option name="capstyle" value="flat" type="QString"/>
            <Option name="customdash" value="2;1" type="QString"/>
            <Option name="customdash_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="customdash_unit" value="MM" type="QString"/>
            <Option name="dash_pattern_offset" value="0" type="QString"/>
            <Option name="dash_pattern_offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="dash_pattern_offset_unit" value="MM" type="QString"/>
            <Option name="draw_inside_polygon" value="0" type="QString"/>
            <Option name="joinstyle" value="miter" type="QString"/>
            <Option name="line_color" value="83,83,83,255" type="QString"/>
            <Option name="line_style" value="solid" type="QString"/>
            <Option name="line_width" value="0.4" type="QString"/>
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
            <Option name="use_custom_dash" value="1" type="QString"/>
            <Option name="width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
          </Option>
          <prop v="0" k="align_dash_pattern"/>
          <prop v="flat" k="capstyle"/>
          <prop v="2;1" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="dash_pattern_offset"/>
          <prop v="3x:0,0,0,0,0,0" k="dash_pattern_offset_map_unit_scale"/>
          <prop v="MM" k="dash_pattern_offset_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="miter" k="joinstyle"/>
          <prop v="83,83,83,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.4" k="line_width"/>
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
          <prop v="1" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="customDash" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="if(@map_scale&lt;=10000,'2;1','1;0.5')" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
                <Option name="outlineWidth" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="if(@map_scale&lt;=10000,0.4,0.2)" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer locked="0" class="LinePatternFill" enabled="1" pass="0">
          <Option type="Map">
            <Option name="angle" value="135" type="QString"/>
            <Option name="color" value="0,0,255,255" type="QString"/>
            <Option name="distance" value="2" type="QString"/>
            <Option name="distance_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="distance_unit" value="MM" type="QString"/>
            <Option name="line_width" value="0.26" type="QString"/>
            <Option name="line_width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="line_width_unit" value="MM" type="QString"/>
            <Option name="offset" value="0" type="QString"/>
            <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="offset_unit" value="MM" type="QString"/>
            <Option name="outline_width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="outline_width_unit" value="MM" type="QString"/>
          </Option>
          <prop v="135" k="angle"/>
          <prop v="0,0,255,255" k="color"/>
          <prop v="2" k="distance"/>
          <prop v="3x:0,0,0,0,0,0" k="distance_map_unit_scale"/>
          <prop v="MM" k="distance_unit"/>
          <prop v="0.26" k="line_width"/>
          <prop v="3x:0,0,0,0,0,0" k="line_width_map_unit_scale"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="lineDistance" type="Map">
                  <Option name="active" value="false" type="bool"/>
                  <Option name="expression" value="" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
          <symbol force_rhr="0" alpha="1" clip_to_extent="1" name="@0@1" type="line">
            <data_defined_properties>
              <Option type="Map">
                <Option name="name" value="" type="QString"/>
                <Option name="properties"/>
                <Option name="type" value="collection" type="QString"/>
              </Option>
            </data_defined_properties>
            <layer locked="0" class="SimpleLine" enabled="1" pass="0">
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
                <Option name="line_color" value="83,83,83,255" type="QString"/>
                <Option name="line_style" value="solid" type="QString"/>
                <Option name="line_width" value="0.4" type="QString"/>
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
              <prop v="83,83,83,255" k="line_color"/>
              <prop v="solid" k="line_style"/>
              <prop v="0.4" k="line_width"/>
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
                      <Option name="expression" value="if(@map_scale&lt;=10000,0.4,0.2)" type="QString"/>
                      <Option name="type" value="3" type="int"/>
                    </Option>
                  </Option>
                  <Option name="type" value="collection" type="QString"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
    </symbols>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <labeling type="simple">
    <settings calloutType="simple">
      <text-style fontWordSpacing="0" previewBkgrdColor="255,255,255,255" textOpacity="1" useSubstitutions="0" isExpression="0" textOrientation="horizontal" multilineHeight="1" legendString="Aa" textColor="50,50,50,255" fontKerning="1" fontWeight="50" fontItalic="0" namedStyle="Normal" capitalization="0" fieldName="oznaczenie" fontFamily="Arial" fontUnderline="0" fontSizeMapUnitScale="3x:0,0,0,0,0,0" fontStrikeout="0" fontSize="3" blendMode="0" fontLetterSpacing="0" fontSizeUnit="MM" allowHtml="0">
        <families/>
        <text-buffer bufferColor="250,250,250,255" bufferNoFill="1" bufferJoinStyle="128" bufferBlendMode="0" bufferDraw="1" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferOpacity="1" bufferSize="0.5" bufferSizeUnits="MM"/>
        <text-mask maskedSymbolLayers="" maskSizeUnits="MM" maskSizeMapUnitScale="3x:0,0,0,0,0,0" maskJoinStyle="128" maskSize="0" maskEnabled="0" maskOpacity="1" maskType="0"/>
        <background shapeDraw="0" shapeSizeType="0" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeJoinStyle="64" shapeFillColor="255,255,255,255" shapeRadiiUnit="Point" shapeSizeY="0" shapeSVGFile="" shapeOpacity="1" shapeOffsetX="0" shapeRadiiX="0" shapeSizeUnit="Point" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeRotation="0" shapeRadiiY="0" shapeSizeX="0" shapeType="0" shapeBorderWidthUnit="Point" shapeBlendMode="0" shapeRotationType="0" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeOffsetUnit="Point" shapeBorderColor="128,128,128,255" shapeBorderWidth="0" shapeOffsetY="0" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0">
          <symbol force_rhr="0" alpha="1" clip_to_extent="1" name="markerSymbol" type="marker">
            <data_defined_properties>
              <Option type="Map">
                <Option name="name" value="" type="QString"/>
                <Option name="properties"/>
                <Option name="type" value="collection" type="QString"/>
              </Option>
            </data_defined_properties>
            <layer locked="0" class="SimpleMarker" enabled="1" pass="0">
              <Option type="Map">
                <Option name="angle" value="0" type="QString"/>
                <Option name="cap_style" value="square" type="QString"/>
                <Option name="color" value="114,155,111,255" type="QString"/>
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
              <prop v="114,155,111,255" k="color"/>
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
          <symbol force_rhr="0" alpha="1" clip_to_extent="1" name="fillSymbol" type="fill">
            <data_defined_properties>
              <Option type="Map">
                <Option name="name" value="" type="QString"/>
                <Option name="properties"/>
                <Option name="type" value="collection" type="QString"/>
              </Option>
            </data_defined_properties>
            <layer locked="0" class="SimpleFill" enabled="1" pass="0">
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
        <shadow shadowOffsetAngle="135" shadowRadiusUnit="MM" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowOpacity="0.69999999999999996" shadowOffsetDist="1" shadowDraw="0" shadowScale="100" shadowUnder="0" shadowOffsetGlobal="1" shadowRadiusAlphaOnly="0" shadowOffsetUnit="MM" shadowBlendMode="6" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowColor="0,0,0,255" shadowRadius="1.5"/>
        <dd_properties>
          <Option type="Map">
            <Option name="name" value="" type="QString"/>
            <Option name="properties"/>
            <Option name="type" value="collection" type="QString"/>
          </Option>
        </dd_properties>
        <substitutions/>
      </text-style>
      <text-format decimals="3" plussign="0" leftDirectionSymbol="&lt;" addDirectionSymbol="0" formatNumbers="0" autoWrapLength="0" reverseDirectionSymbol="0" useMaxLineLengthForAutoWrap="1" wrapChar="" multilineAlign="3" rightDirectionSymbol=">" placeDirectionSymbol="0"/>
      <placement overrunDistance="0" overrunDistanceUnit="MM" quadOffset="4" repeatDistance="0" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" dist="0" rotationAngle="0" geometryGeneratorEnabled="0" offsetUnits="MM" repeatDistanceUnits="MM" centroidInside="1" maxCurvedCharAngleOut="-25" geometryGeneratorType="PointGeometry" distUnits="MM" placementFlags="10" priority="5" maxCurvedCharAngleIn="25" placement="0" distMapUnitScale="3x:0,0,0,0,0,0" lineAnchorPercent="0.5" geometryGenerator="" rotationUnit="AngleDegrees" lineAnchorType="0" lineAnchorClipping="0" layerType="PolygonGeometry" overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" polygonPlacementFlags="2" fitInPolygonOnly="0" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" offsetType="0" preserveRotation="1" yOffset="0" xOffset="0" centroidWhole="0"/>
      <rendering fontLimitPixelSize="0" fontMinPixelSize="3" labelPerPart="0" fontMaxPixelSize="10000" mergeLines="0" obstacleType="1" scaleMax="0" scaleMin="0" upsidedownLabels="0" minFeatureSize="0" displayAll="0" zIndex="0" limitNumLabels="0" unplacedVisibility="0" obstacleFactor="1" obstacle="1" drawLabels="1" maxNumLabels="2000" scaleVisibility="0"/>
      <dd_properties>
        <Option type="Map">
          <Option name="name" value="" type="QString"/>
          <Option name="properties" type="Map">
            <Option name="Size" type="Map">
              <Option name="active" value="true" type="bool"/>
              <Option name="expression" value="if(@map_scale&lt;=10000,3,0)" type="QString"/>
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
          <Option name="lineSymbol" value="&lt;symbol force_rhr=&quot;0&quot; alpha=&quot;1&quot; clip_to_extent=&quot;1&quot; name=&quot;symbol&quot; type=&quot;line&quot;>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option name=&quot;name&quot; value=&quot;&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option name=&quot;type&quot; value=&quot;collection&quot; type=&quot;QString&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;layer locked=&quot;0&quot; class=&quot;SimpleLine&quot; enabled=&quot;1&quot; pass=&quot;0&quot;>&lt;Option type=&quot;Map&quot;>&lt;Option name=&quot;align_dash_pattern&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;capstyle&quot; value=&quot;square&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;customdash&quot; value=&quot;5;2&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;customdash_map_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;customdash_unit&quot; value=&quot;MM&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;dash_pattern_offset&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;dash_pattern_offset_map_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;dash_pattern_offset_unit&quot; value=&quot;MM&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;draw_inside_polygon&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;joinstyle&quot; value=&quot;bevel&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;line_color&quot; value=&quot;60,60,60,255&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;line_style&quot; value=&quot;solid&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;line_width&quot; value=&quot;0.3&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;line_width_unit&quot; value=&quot;MM&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;offset&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;offset_map_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;offset_unit&quot; value=&quot;MM&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;ring_filter&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;trim_distance_end&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;trim_distance_end_map_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;trim_distance_end_unit&quot; value=&quot;MM&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;trim_distance_start&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;trim_distance_start_map_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;trim_distance_start_unit&quot; value=&quot;MM&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;tweak_dash_pattern_on_corners&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;use_custom_dash&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;width_map_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot;/>&lt;/Option>&lt;prop v=&quot;0&quot; k=&quot;align_dash_pattern&quot;/>&lt;prop v=&quot;square&quot; k=&quot;capstyle&quot;/>&lt;prop v=&quot;5;2&quot; k=&quot;customdash&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;customdash_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;customdash_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;dash_pattern_offset&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;dash_pattern_offset_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;dash_pattern_offset_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;draw_inside_polygon&quot;/>&lt;prop v=&quot;bevel&quot; k=&quot;joinstyle&quot;/>&lt;prop v=&quot;60,60,60,255&quot; k=&quot;line_color&quot;/>&lt;prop v=&quot;solid&quot; k=&quot;line_style&quot;/>&lt;prop v=&quot;0.3&quot; k=&quot;line_width&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;line_width_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;offset&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;offset_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;offset_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;ring_filter&quot;/>&lt;prop v=&quot;0&quot; k=&quot;trim_distance_end&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;trim_distance_end_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;trim_distance_end_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;trim_distance_start&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;trim_distance_start_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;trim_distance_start_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;tweak_dash_pattern_on_corners&quot;/>&lt;prop v=&quot;0&quot; k=&quot;use_custom_dash&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;width_map_unit_scale&quot;/>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option name=&quot;name&quot; value=&quot;&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option name=&quot;type&quot; value=&quot;collection&quot; type=&quot;QString&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>" type="QString"/>
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
        <Option value="&quot;przestrzenNazw&quot;" type="QString"/>
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
    <DiagramCategory maxScaleDenominator="1e+08" spacingUnit="MM" lineSizeScale="3x:0,0,0,0,0,0" barWidth="5" penColor="#000000" sizeType="MM" penWidth="0" scaleDependency="Area" showAxis="1" spacing="5" backgroundAlpha="255" opacity="1" direction="0" spacingUnitScale="3x:0,0,0,0,0,0" scaleBasedVisibility="0" width="15" diagramOrientation="Up" minScaleDenominator="0" lineSizeType="MM" rotationOffset="270" penAlpha="255" enabled="0" backgroundColor="#ffffff" sizeScale="3x:0,0,0,0,0,0" labelPlacementMethod="XHeight" minimumSize="0" height="15">
      <fontProperties description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" style=""/>
      <attribute color="#000000" label="" field="" colorOpacity="1"/>
      <axisSymbol>
        <symbol force_rhr="0" alpha="1" clip_to_extent="1" name="" type="line">
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
          <layer locked="0" class="SimpleLine" enabled="1" pass="0">
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
  <DiagramLayerSettings dist="0" showAll="1" zIndex="0" obstacle="0" priority="0" linePlacementFlags="18" placement="1">
    <properties>
      <Option type="Map">
        <Option name="name" value="" type="QString"/>
        <Option name="properties"/>
        <Option name="type" value="collection" type="QString"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions removeDuplicateNodes="0">
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
    <field name="fid" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="przestrzenNazw" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="lokalnyId" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="wersjaId" configurationFlags="None">
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
    <field name="nazwa" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="oznaczenie" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="symbol" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="poczatekWersjiObiektu" configurationFlags="None">
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
    <field name="koniecWersjiObiektu" configurationFlags="None">
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
    <field name="obowiazujeOd" configurationFlags="None">
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
    <field name="obowiazujeDo" configurationFlags="None">
      <editWidget type="DateTime">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="status" configurationFlags="None">
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
    <field name="charakterUstalenia" configurationFlags="None">
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
    <field name="plan" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="wylaczenieZabudowyZagrodowej" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="odlegloscDoSzkolyPodstawowej" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="odlegloscDoObszarowZieleniPublicznej" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="powierzchniaLacznaObszarowZieleniPublicznej" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="odlegloscDoObszaruZieleniPublicznej" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="powierzchniaObszaruZieleniPublicznej" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="odlegloscDoPrzedszkola" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="odlegloscDoZlobka" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="odlegloscDoAmbulatoriumPOZ" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="odlegloscDoBiblioteki" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="odlegloscDoDomuKultury" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="odlegloscDoDomuPomocySpolecznej" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="odlegloscDoUrzadzonegoTerenuSportu" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="odlegloscDoPrzystanku" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="odlegloscDoPlacowkiPocztowej" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="odlegloscDoApteki" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="odlegloscDoPosterunkuPolicji" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="odlegloscDoPosterunkuJednostkiOchronyPrzeciwpozarowej" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias name="" field="fid" index="0"/>
    <alias name="" field="przestrzenNazw" index="1"/>
    <alias name="" field="lokalnyId" index="2"/>
    <alias name="" field="wersjaId" index="3"/>
    <alias name="" field="nazwa" index="4"/>
    <alias name="" field="oznaczenie" index="5"/>
    <alias name="" field="symbol" index="6"/>
    <alias name="" field="poczatekWersjiObiektu" index="7"/>
    <alias name="" field="koniecWersjiObiektu" index="8"/>
    <alias name="" field="obowiazujeOd" index="9"/>
    <alias name="" field="obowiazujeDo" index="10"/>
    <alias name="" field="status" index="11"/>
    <alias name="" field="charakterUstalenia" index="12"/>
    <alias name="" field="plan" index="13"/>
    <alias name="" field="wylaczenieZabudowyZagrodowej" index="14"/>
    <alias name="" field="odlegloscDoSzkolyPodstawowej" index="15"/>
    <alias name="" field="odlegloscDoObszarowZieleniPublicznej" index="16"/>
    <alias name="" field="powierzchniaLacznaObszarowZieleniPublicznej" index="17"/>
    <alias name="" field="odlegloscDoObszaruZieleniPublicznej" index="18"/>
    <alias name="" field="powierzchniaObszaruZieleniPublicznej" index="19"/>
    <alias name="" field="odlegloscDoPrzedszkola" index="20"/>
    <alias name="" field="odlegloscDoZlobka" index="21"/>
    <alias name="" field="odlegloscDoAmbulatoriumPOZ" index="22"/>
    <alias name="" field="odlegloscDoBiblioteki" index="23"/>
    <alias name="" field="odlegloscDoDomuKultury" index="24"/>
    <alias name="" field="odlegloscDoDomuPomocySpolecznej" index="25"/>
    <alias name="" field="odlegloscDoUrzadzonegoTerenuSportu" index="26"/>
    <alias name="" field="odlegloscDoPrzystanku" index="27"/>
    <alias name="" field="odlegloscDoPlacowkiPocztowej" index="28"/>
    <alias name="" field="odlegloscDoApteki" index="29"/>
    <alias name="" field="odlegloscDoPosterunkuPolicji" index="30"/>
    <alias name="" field="odlegloscDoPosterunkuJednostkiOchronyPrzeciwpozarowej" index="31"/>
  </aliases>
  <defaults>
    <default expression="" field="fid" applyOnUpdate="0"/>
    <default expression="" field="przestrzenNazw" applyOnUpdate="0"/>
    <default expression="" field="lokalnyId" applyOnUpdate="0"/>
    <default expression="" field="wersjaId" applyOnUpdate="0"/>
    <default expression="'Obszar standardów dostępności infrastruktury społecznej'" field="nazwa" applyOnUpdate="1"/>
    <default expression="" field="oznaczenie" applyOnUpdate="0"/>
    <default expression="'OSD'" field="symbol" applyOnUpdate="0"/>
    <default expression="" field="poczatekWersjiObiektu" applyOnUpdate="0"/>
    <default expression="" field="koniecWersjiObiektu" applyOnUpdate="0"/>
    <default expression="" field="obowiazujeOd" applyOnUpdate="0"/>
    <default expression="" field="obowiazujeDo" applyOnUpdate="0"/>
    <default expression="" field="status" applyOnUpdate="0"/>
    <default expression="'ogólnie wiążące'" field="charakterUstalenia" applyOnUpdate="0"/>
    <default expression="" field="plan" applyOnUpdate="0"/>
    <default expression="" field="wylaczenieZabudowyZagrodowej" applyOnUpdate="0"/>
    <default expression="" field="odlegloscDoSzkolyPodstawowej" applyOnUpdate="0"/>
    <default expression="" field="odlegloscDoObszarowZieleniPublicznej" applyOnUpdate="0"/>
    <default expression="" field="powierzchniaLacznaObszarowZieleniPublicznej" applyOnUpdate="0"/>
    <default expression="" field="odlegloscDoObszaruZieleniPublicznej" applyOnUpdate="0"/>
    <default expression="" field="powierzchniaObszaruZieleniPublicznej" applyOnUpdate="0"/>
    <default expression="" field="odlegloscDoPrzedszkola" applyOnUpdate="0"/>
    <default expression="" field="odlegloscDoZlobka" applyOnUpdate="0"/>
    <default expression="" field="odlegloscDoAmbulatoriumPOZ" applyOnUpdate="0"/>
    <default expression="" field="odlegloscDoBiblioteki" applyOnUpdate="0"/>
    <default expression="" field="odlegloscDoDomuKultury" applyOnUpdate="0"/>
    <default expression="" field="odlegloscDoDomuPomocySpolecznej" applyOnUpdate="0"/>
    <default expression="" field="odlegloscDoUrzadzonegoTerenuSportu" applyOnUpdate="0"/>
    <default expression="" field="odlegloscDoPrzystanku" applyOnUpdate="0"/>
    <default expression="" field="odlegloscDoPlacowkiPocztowej" applyOnUpdate="0"/>
    <default expression="" field="odlegloscDoApteki" applyOnUpdate="0"/>
    <default expression="" field="odlegloscDoPosterunkuPolicji" applyOnUpdate="0"/>
    <default expression="" field="odlegloscDoPosterunkuJednostkiOchronyPrzeciwpozarowej" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint unique_strength="1" constraints="3" notnull_strength="1" field="fid" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" notnull_strength="0" field="przestrzenNazw" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" notnull_strength="0" field="lokalnyId" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" notnull_strength="0" field="wersjaId" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" notnull_strength="0" field="nazwa" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" notnull_strength="0" field="oznaczenie" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" notnull_strength="0" field="symbol" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" notnull_strength="0" field="poczatekWersjiObiektu" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" notnull_strength="0" field="koniecWersjiObiektu" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" notnull_strength="0" field="obowiazujeOd" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" notnull_strength="0" field="obowiazujeDo" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" notnull_strength="0" field="status" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" notnull_strength="0" field="charakterUstalenia" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" notnull_strength="0" field="plan" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" notnull_strength="0" field="wylaczenieZabudowyZagrodowej" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" notnull_strength="0" field="odlegloscDoSzkolyPodstawowej" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" notnull_strength="0" field="odlegloscDoObszarowZieleniPublicznej" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" notnull_strength="0" field="powierzchniaLacznaObszarowZieleniPublicznej" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" notnull_strength="0" field="odlegloscDoObszaruZieleniPublicznej" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" notnull_strength="0" field="powierzchniaObszaruZieleniPublicznej" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" notnull_strength="0" field="odlegloscDoPrzedszkola" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" notnull_strength="0" field="odlegloscDoZlobka" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" notnull_strength="0" field="odlegloscDoAmbulatoriumPOZ" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" notnull_strength="0" field="odlegloscDoBiblioteki" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" notnull_strength="0" field="odlegloscDoDomuKultury" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" notnull_strength="0" field="odlegloscDoDomuPomocySpolecznej" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" notnull_strength="0" field="odlegloscDoUrzadzonegoTerenuSportu" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" notnull_strength="0" field="odlegloscDoPrzystanku" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" notnull_strength="0" field="odlegloscDoPlacowkiPocztowej" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" notnull_strength="0" field="odlegloscDoApteki" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" notnull_strength="0" field="odlegloscDoPosterunkuPolicji" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" notnull_strength="0" field="odlegloscDoPosterunkuJednostkiOchronyPrzeciwpozarowej" exp_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" desc="" field="fid"/>
    <constraint exp="" desc="" field="przestrzenNazw"/>
    <constraint exp="" desc="" field="lokalnyId"/>
    <constraint exp="" desc="" field="wersjaId"/>
    <constraint exp="" desc="" field="nazwa"/>
    <constraint exp="" desc="" field="oznaczenie"/>
    <constraint exp="" desc="" field="symbol"/>
    <constraint exp="" desc="" field="poczatekWersjiObiektu"/>
    <constraint exp="" desc="" field="koniecWersjiObiektu"/>
    <constraint exp="" desc="" field="obowiazujeOd"/>
    <constraint exp="" desc="" field="obowiazujeDo"/>
    <constraint exp="" desc="" field="status"/>
    <constraint exp="" desc="" field="charakterUstalenia"/>
    <constraint exp="" desc="" field="plan"/>
    <constraint exp="" desc="" field="wylaczenieZabudowyZagrodowej"/>
    <constraint exp="" desc="" field="odlegloscDoSzkolyPodstawowej"/>
    <constraint exp="" desc="" field="odlegloscDoObszarowZieleniPublicznej"/>
    <constraint exp="" desc="" field="powierzchniaLacznaObszarowZieleniPublicznej"/>
    <constraint exp="" desc="" field="odlegloscDoObszaruZieleniPublicznej"/>
    <constraint exp="" desc="" field="powierzchniaObszaruZieleniPublicznej"/>
    <constraint exp="" desc="" field="odlegloscDoPrzedszkola"/>
    <constraint exp="" desc="" field="odlegloscDoZlobka"/>
    <constraint exp="" desc="" field="odlegloscDoAmbulatoriumPOZ"/>
    <constraint exp="" desc="" field="odlegloscDoBiblioteki"/>
    <constraint exp="" desc="" field="odlegloscDoDomuKultury"/>
    <constraint exp="" desc="" field="odlegloscDoDomuPomocySpolecznej"/>
    <constraint exp="" desc="" field="odlegloscDoUrzadzonegoTerenuSportu"/>
    <constraint exp="" desc="" field="odlegloscDoPrzystanku"/>
    <constraint exp="" desc="" field="odlegloscDoPlacowkiPocztowej"/>
    <constraint exp="" desc="" field="odlegloscDoApteki"/>
    <constraint exp="" desc="" field="odlegloscDoPosterunkuPolicji"/>
    <constraint exp="" desc="" field="odlegloscDoPosterunkuJednostkiOchronyPrzeciwpozarowej"/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig sortOrder="0" actionWidgetStyle="dropDown" sortExpression="">
    <columns>
      <column width="-1" name="fid" type="field" hidden="0"/>
      <column width="-1" name="przestrzenNazw" type="field" hidden="0"/>
      <column width="-1" name="lokalnyId" type="field" hidden="0"/>
      <column width="-1" name="wersjaId" type="field" hidden="0"/>
      <column width="-1" name="nazwa" type="field" hidden="0"/>
      <column width="-1" name="oznaczenie" type="field" hidden="0"/>
      <column width="-1" name="symbol" type="field" hidden="0"/>
      <column width="-1" name="poczatekWersjiObiektu" type="field" hidden="0"/>
      <column width="-1" name="koniecWersjiObiektu" type="field" hidden="0"/>
      <column width="-1" name="obowiazujeOd" type="field" hidden="0"/>
      <column width="-1" name="obowiazujeDo" type="field" hidden="0"/>
      <column width="-1" name="status" type="field" hidden="0"/>
      <column width="-1" name="charakterUstalenia" type="field" hidden="0"/>
      <column width="-1" name="plan" type="field" hidden="0"/>
      <column width="199" name="wylaczenieZabudowyZagrodowej" type="field" hidden="0"/>
      <column width="-1" name="odlegloscDoSzkolyPodstawowej" type="field" hidden="0"/>
      <column width="-1" name="odlegloscDoObszarowZieleniPublicznej" type="field" hidden="0"/>
      <column width="-1" name="powierzchniaLacznaObszarowZieleniPublicznej" type="field" hidden="0"/>
      <column width="-1" name="odlegloscDoObszaruZieleniPublicznej" type="field" hidden="0"/>
      <column width="-1" name="powierzchniaObszaruZieleniPublicznej" type="field" hidden="0"/>
      <column width="-1" name="odlegloscDoPrzedszkola" type="field" hidden="0"/>
      <column width="-1" name="odlegloscDoZlobka" type="field" hidden="0"/>
      <column width="-1" name="odlegloscDoAmbulatoriumPOZ" type="field" hidden="0"/>
      <column width="-1" name="odlegloscDoBiblioteki" type="field" hidden="0"/>
      <column width="-1" name="odlegloscDoDomuKultury" type="field" hidden="0"/>
      <column width="-1" name="odlegloscDoDomuPomocySpolecznej" type="field" hidden="0"/>
      <column width="-1" name="odlegloscDoUrzadzonegoTerenuSportu" type="field" hidden="0"/>
      <column width="-1" name="odlegloscDoPrzystanku" type="field" hidden="0"/>
      <column width="-1" name="odlegloscDoPlacowkiPocztowej" type="field" hidden="0"/>
      <column width="-1" name="odlegloscDoApteki" type="field" hidden="0"/>
      <column width="-1" name="odlegloscDoPosterunkuPolicji" type="field" hidden="0"/>
      <column width="-1" name="odlegloscDoPosterunkuJednostkiOchronyPrzeciwpozarowej" type="field" hidden="0"/>
      <column width="-1" type="actions" hidden="1"/>
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
    <field name="nazwa" editable="0"/>
    <field name="obowiazujeDo" editable="1"/>
    <field name="obowiazujeOd" editable="1"/>
    <field name="odlegloscDoAmbulatoriumPOZ" editable="1"/>
    <field name="odlegloscDoApteki" editable="1"/>
    <field name="odlegloscDoBiblioteki" editable="1"/>
    <field name="odlegloscDoDomuKultury" editable="1"/>
    <field name="odlegloscDoDomuPomocySpolecznej" editable="1"/>
    <field name="odlegloscDoObszarowZieleniPublicznej" editable="1"/>
    <field name="odlegloscDoObszaruZieleniPublicznej" editable="1"/>
    <field name="odlegloscDoPlacowkiPocztowej" editable="1"/>
    <field name="odlegloscDoPosterunkuJednostkiOchronyPrzeciwpozarowej" editable="1"/>
    <field name="odlegloscDoPosterunkuPolicji" editable="1"/>
    <field name="odlegloscDoPrzedszkola" editable="1"/>
    <field name="odlegloscDoPrzystanku" editable="1"/>
    <field name="odlegloscDoSzkolyPodstawowej" editable="1"/>
    <field name="odlegloscDoUrzadzonegoTerenuSportu" editable="1"/>
    <field name="odlegloscDoZlobka" editable="1"/>
    <field name="oznaczenie" editable="1"/>
    <field name="plan" editable="1"/>
    <field name="poczatekWersjiObiektu" editable="1"/>
    <field name="powierzchniaLacznaObszarowZieleniPublicznej" editable="1"/>
    <field name="powierzchniaObszaruZieleniPublicznej" editable="1"/>
    <field name="przestrzenNazw" editable="1"/>
    <field name="status" editable="1"/>
    <field name="symbol" editable="0"/>
    <field name="tytul" editable="1"/>
    <field name="wersjaId" editable="1"/>
    <field name="wylaczenieZabudowyZagrodowej" editable="1"/>
  </editable>
  <labelOnTop>
    <field name="charakterUstalenia" labelOnTop="0"/>
    <field name="fid" labelOnTop="0"/>
    <field name="gml_id" labelOnTop="0"/>
    <field name="koniecWersjiObiektu" labelOnTop="0"/>
    <field name="lokalnyId" labelOnTop="0"/>
    <field name="nazwa" labelOnTop="0"/>
    <field name="obowiazujeDo" labelOnTop="0"/>
    <field name="obowiazujeOd" labelOnTop="0"/>
    <field name="odlegloscDoAmbulatoriumPOZ" labelOnTop="0"/>
    <field name="odlegloscDoApteki" labelOnTop="0"/>
    <field name="odlegloscDoBiblioteki" labelOnTop="0"/>
    <field name="odlegloscDoDomuKultury" labelOnTop="0"/>
    <field name="odlegloscDoDomuPomocySpolecznej" labelOnTop="0"/>
    <field name="odlegloscDoObszarowZieleniPublicznej" labelOnTop="0"/>
    <field name="odlegloscDoObszaruZieleniPublicznej" labelOnTop="0"/>
    <field name="odlegloscDoPlacowkiPocztowej" labelOnTop="0"/>
    <field name="odlegloscDoPosterunkuJednostkiOchronyPrzeciwpozarowej" labelOnTop="0"/>
    <field name="odlegloscDoPosterunkuPolicji" labelOnTop="0"/>
    <field name="odlegloscDoPrzedszkola" labelOnTop="0"/>
    <field name="odlegloscDoPrzystanku" labelOnTop="0"/>
    <field name="odlegloscDoSzkolyPodstawowej" labelOnTop="0"/>
    <field name="odlegloscDoUrzadzonegoTerenuSportu" labelOnTop="0"/>
    <field name="odlegloscDoZlobka" labelOnTop="0"/>
    <field name="oznaczenie" labelOnTop="0"/>
    <field name="plan" labelOnTop="0"/>
    <field name="poczatekWersjiObiektu" labelOnTop="0"/>
    <field name="powierzchniaLacznaObszarowZieleniPublicznej" labelOnTop="0"/>
    <field name="powierzchniaObszaruZieleniPublicznej" labelOnTop="0"/>
    <field name="przestrzenNazw" labelOnTop="0"/>
    <field name="status" labelOnTop="0"/>
    <field name="symbol" labelOnTop="0"/>
    <field name="tytul" labelOnTop="0"/>
    <field name="wersjaId" labelOnTop="0"/>
    <field name="wylaczenieZabudowyZagrodowej" labelOnTop="0"/>
  </labelOnTop>
  <reuseLastValue>
    <field name="charakterUstalenia" reuseLastValue="0"/>
    <field name="fid" reuseLastValue="0"/>
    <field name="gml_id" reuseLastValue="0"/>
    <field name="koniecWersjiObiektu" reuseLastValue="0"/>
    <field name="lokalnyId" reuseLastValue="0"/>
    <field name="nazwa" reuseLastValue="0"/>
    <field name="obowiazujeDo" reuseLastValue="0"/>
    <field name="obowiazujeOd" reuseLastValue="0"/>
    <field name="odlegloscDoAmbulatoriumPOZ" reuseLastValue="0"/>
    <field name="odlegloscDoApteki" reuseLastValue="0"/>
    <field name="odlegloscDoBiblioteki" reuseLastValue="0"/>
    <field name="odlegloscDoDomuKultury" reuseLastValue="0"/>
    <field name="odlegloscDoDomuPomocySpolecznej" reuseLastValue="0"/>
    <field name="odlegloscDoObszarowZieleniPublicznej" reuseLastValue="0"/>
    <field name="odlegloscDoObszaruZieleniPublicznej" reuseLastValue="0"/>
    <field name="odlegloscDoPlacowkiPocztowej" reuseLastValue="0"/>
    <field name="odlegloscDoPosterunkuJednostkiOchronyPrzeciwpozarowej" reuseLastValue="0"/>
    <field name="odlegloscDoPosterunkuPolicji" reuseLastValue="0"/>
    <field name="odlegloscDoPrzedszkola" reuseLastValue="0"/>
    <field name="odlegloscDoPrzystanku" reuseLastValue="0"/>
    <field name="odlegloscDoSzkolyPodstawowej" reuseLastValue="0"/>
    <field name="odlegloscDoUrzadzonegoTerenuSportu" reuseLastValue="0"/>
    <field name="odlegloscDoZlobka" reuseLastValue="0"/>
    <field name="oznaczenie" reuseLastValue="0"/>
    <field name="plan" reuseLastValue="0"/>
    <field name="poczatekWersjiObiektu" reuseLastValue="0"/>
    <field name="powierzchniaLacznaObszarowZieleniPublicznej" reuseLastValue="0"/>
    <field name="powierzchniaObszaruZieleniPublicznej" reuseLastValue="0"/>
    <field name="przestrzenNazw" reuseLastValue="0"/>
    <field name="status" reuseLastValue="0"/>
    <field name="symbol" reuseLastValue="0"/>
    <field name="tytul" reuseLastValue="0"/>
    <field name="wersjaId" reuseLastValue="0"/>
    <field name="wylaczenieZabudowyZagrodowej" reuseLastValue="0"/>
  </reuseLastValue>
  <dataDefinedFieldProperties/>
  <widgets/>
  <mapTip></mapTip>
  <layerGeometryType>2</layerGeometryType>
</qgis>

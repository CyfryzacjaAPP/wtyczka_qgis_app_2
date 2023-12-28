<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis styleCategories="Symbology|Symbology3D|Labeling|Fields|Forms|Actions|MapTips|Diagrams|AttributeTable|Rendering|CustomProperties|GeometryOptions|Relations|Temporal|Legend|Elevation|Notes" simplifyAlgorithm="0" symbologyReferenceScale="-1" version="3.22.15-Białowieża" simplifyDrawingHints="0" simplifyDrawingTol="2" labelsEnabled="1" minScale="100000000" hasScaleBasedVisibilityFlag="0" simplifyMaxScale="1" simplifyLocal="1" maxScale="0">
  <temporal durationField="fid" limitMode="0" endExpression="" durationUnit="min" startField="" mode="0" enabled="0" startExpression="" endField="" fixedDuration="0" accumulate="0">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <renderer-v2 forceraster="0" type="singleSymbol" symbollevels="0" referencescale="-1" enableorderby="0">
    <symbols>
      <symbol force_rhr="0" name="0" type="fill" alpha="1" clip_to_extent="1">
        <data_defined_properties>
          <Option type="Map">
            <Option value="" name="name" type="QString"/>
            <Option name="properties"/>
            <Option value="collection" name="type" type="QString"/>
          </Option>
        </data_defined_properties>
        <layer class="SimpleLine" enabled="1" pass="0" locked="0">
          <Option type="Map">
            <Option value="0" name="align_dash_pattern" type="QString"/>
            <Option value="flat" name="capstyle" type="QString"/>
            <Option value="2;1" name="customdash" type="QString"/>
            <Option value="3x:0,0,0,0,0,0" name="customdash_map_unit_scale" type="QString"/>
            <Option value="MM" name="customdash_unit" type="QString"/>
            <Option value="0" name="dash_pattern_offset" type="QString"/>
            <Option value="3x:0,0,0,0,0,0" name="dash_pattern_offset_map_unit_scale" type="QString"/>
            <Option value="MM" name="dash_pattern_offset_unit" type="QString"/>
            <Option value="0" name="draw_inside_polygon" type="QString"/>
            <Option value="miter" name="joinstyle" type="QString"/>
            <Option value="83,83,83,255" name="line_color" type="QString"/>
            <Option value="solid" name="line_style" type="QString"/>
            <Option value="0.4" name="line_width" type="QString"/>
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
            <Option value="1" name="use_custom_dash" type="QString"/>
            <Option value="3x:0,0,0,0,0,0" name="width_map_unit_scale" type="QString"/>
          </Option>
          <prop k="align_dash_pattern" v="0"/>
          <prop k="capstyle" v="flat"/>
          <prop k="customdash" v="2;1"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="dash_pattern_offset" v="0"/>
          <prop k="dash_pattern_offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="dash_pattern_offset_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="miter"/>
          <prop k="line_color" v="83,83,83,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="0.4"/>
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
          <prop k="use_custom_dash" v="1"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" name="name" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="outlineWidth" type="Map">
                  <Option value="true" name="active" type="bool"/>
                  <Option value="if(@map_scale&lt;=10000,0.4,0.2)" name="expression" type="QString"/>
                  <Option value="3" name="type" type="int"/>
                </Option>
              </Option>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer class="LinePatternFill" enabled="1" pass="0" locked="0">
          <Option type="Map">
            <Option value="135" name="angle" type="QString"/>
            <Option value="0,0,255,255" name="color" type="QString"/>
            <Option value="2" name="distance" type="QString"/>
            <Option value="3x:0,0,0,0,0,0" name="distance_map_unit_scale" type="QString"/>
            <Option value="MM" name="distance_unit" type="QString"/>
            <Option value="0.26" name="line_width" type="QString"/>
            <Option value="3x:0,0,0,0,0,0" name="line_width_map_unit_scale" type="QString"/>
            <Option value="MM" name="line_width_unit" type="QString"/>
            <Option value="0" name="offset" type="QString"/>
            <Option value="3x:0,0,0,0,0,0" name="offset_map_unit_scale" type="QString"/>
            <Option value="MM" name="offset_unit" type="QString"/>
            <Option value="3x:0,0,0,0,0,0" name="outline_width_map_unit_scale" type="QString"/>
            <Option value="MM" name="outline_width_unit" type="QString"/>
          </Option>
          <prop k="angle" v="135"/>
          <prop k="color" v="0,0,255,255"/>
          <prop k="distance" v="2"/>
          <prop k="distance_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="distance_unit" v="MM"/>
          <prop k="line_width" v="0.26"/>
          <prop k="line_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" name="name" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="lineDistance" type="Map">
                  <Option value="false" name="active" type="bool"/>
                  <Option value="" name="expression" type="QString"/>
                  <Option value="3" name="type" type="int"/>
                </Option>
              </Option>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
          <symbol force_rhr="0" name="@0@1" type="line" alpha="1" clip_to_extent="1">
            <data_defined_properties>
              <Option type="Map">
                <Option value="" name="name" type="QString"/>
                <Option name="properties"/>
                <Option value="collection" name="type" type="QString"/>
              </Option>
            </data_defined_properties>
            <layer class="SimpleLine" enabled="1" pass="0" locked="0">
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
                <Option value="83,83,83,255" name="line_color" type="QString"/>
                <Option value="solid" name="line_style" type="QString"/>
                <Option value="0.4" name="line_width" type="QString"/>
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
              <prop k="line_color" v="83,83,83,255"/>
              <prop k="line_style" v="solid"/>
              <prop k="line_width" v="0.4"/>
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
                      <Option value="if(@map_scale&lt;=10000,0.4,0.2)" name="expression" type="QString"/>
                      <Option value="3" name="type" type="int"/>
                    </Option>
                  </Option>
                  <Option value="collection" name="type" type="QString"/>
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
      <text-style multilineHeight="1" fontSize="3" useSubstitutions="0" fontStrikeout="0" capitalization="0" allowHtml="0" fontUnderline="0" fontFamily="Arial" fontWordSpacing="0" textColor="50,50,50,255" fontItalic="0" isExpression="0" textOpacity="1" fontKerning="1" fontSizeUnit="MM" fontSizeMapUnitScale="3x:0,0,0,0,0,0" fieldName="oznaczenie" namedStyle="Normal" blendMode="0" textOrientation="horizontal" previewBkgrdColor="255,255,255,255" fontLetterSpacing="0" legendString="Aa" fontWeight="50">
        <families/>
        <text-buffer bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferJoinStyle="128" bufferBlendMode="0" bufferColor="250,250,250,255" bufferOpacity="1" bufferNoFill="1" bufferSizeUnits="MM" bufferDraw="1" bufferSize="0.5"/>
        <text-mask maskSizeUnits="MM" maskOpacity="1" maskSizeMapUnitScale="3x:0,0,0,0,0,0" maskType="0" maskedSymbolLayers="" maskEnabled="0" maskJoinStyle="128" maskSize="0"/>
        <background shapeDraw="0" shapeRotationType="0" shapeOffsetY="0" shapeOpacity="1" shapeFillColor="255,255,255,255" shapeSizeType="0" shapeSVGFile="" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeOffsetX="0" shapeSizeX="0" shapeBlendMode="0" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeType="0" shapeBorderWidth="0" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeSizeUnit="Point" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeRotation="0" shapeBorderColor="128,128,128,255" shapeBorderWidthUnit="Point" shapeSizeY="0" shapeJoinStyle="64" shapeOffsetUnit="Point" shapeRadiiUnit="Point" shapeRadiiX="0" shapeRadiiY="0">
          <symbol force_rhr="0" name="markerSymbol" type="marker" alpha="1" clip_to_extent="1">
            <data_defined_properties>
              <Option type="Map">
                <Option value="" name="name" type="QString"/>
                <Option name="properties"/>
                <Option value="collection" name="type" type="QString"/>
              </Option>
            </data_defined_properties>
            <layer class="SimpleMarker" enabled="1" pass="0" locked="0">
              <Option type="Map">
                <Option value="0" name="angle" type="QString"/>
                <Option value="square" name="cap_style" type="QString"/>
                <Option value="114,155,111,255" name="color" type="QString"/>
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
              <prop k="color" v="114,155,111,255"/>
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
          <symbol force_rhr="0" name="fillSymbol" type="fill" alpha="1" clip_to_extent="1">
            <data_defined_properties>
              <Option type="Map">
                <Option value="" name="name" type="QString"/>
                <Option name="properties"/>
                <Option value="collection" name="type" type="QString"/>
              </Option>
            </data_defined_properties>
            <layer class="SimpleFill" enabled="1" pass="0" locked="0">
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
        <shadow shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowOffsetUnit="MM" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowColor="0,0,0,255" shadowRadiusUnit="MM" shadowBlendMode="6" shadowDraw="0" shadowOffsetGlobal="1" shadowOpacity="0.69999999999999996" shadowScale="100" shadowOffsetDist="1" shadowUnder="0" shadowRadiusAlphaOnly="0" shadowRadius="1.5" shadowOffsetAngle="135"/>
        <dd_properties>
          <Option type="Map">
            <Option value="" name="name" type="QString"/>
            <Option name="properties"/>
            <Option value="collection" name="type" type="QString"/>
          </Option>
        </dd_properties>
        <substitutions/>
      </text-style>
      <text-format formatNumbers="0" decimals="3" rightDirectionSymbol=">" useMaxLineLengthForAutoWrap="1" reverseDirectionSymbol="0" plussign="0" autoWrapLength="0" wrapChar="" multilineAlign="3" addDirectionSymbol="0" leftDirectionSymbol="&lt;" placeDirectionSymbol="0"/>
      <placement fitInPolygonOnly="0" rotationUnit="AngleDegrees" maxCurvedCharAngleIn="25" maxCurvedCharAngleOut="-25" priority="5" preserveRotation="1" lineAnchorPercent="0.5" geometryGeneratorType="PointGeometry" offsetType="0" quadOffset="4" geometryGeneratorEnabled="0" distMapUnitScale="3x:0,0,0,0,0,0" repeatDistance="0" geometryGenerator="" lineAnchorClipping="0" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" layerType="PolygonGeometry" centroidInside="1" overrunDistance="0" placement="0" offsetUnits="MM" lineAnchorType="0" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" rotationAngle="0" distUnits="MM" xOffset="0" overrunDistanceUnit="MM" dist="0" placementFlags="10" centroidWhole="0" polygonPlacementFlags="2" repeatDistanceUnits="MM" yOffset="0"/>
      <rendering scaleVisibility="0" limitNumLabels="0" fontLimitPixelSize="0" displayAll="0" obstacleFactor="1" mergeLines="0" labelPerPart="0" obstacle="1" zIndex="0" fontMinPixelSize="3" scaleMin="0" upsidedownLabels="0" minFeatureSize="0" unplacedVisibility="0" fontMaxPixelSize="10000" obstacleType="1" maxNumLabels="2000" drawLabels="1" scaleMax="0"/>
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
          <Option value="&lt;symbol force_rhr=&quot;0&quot; name=&quot;symbol&quot; type=&quot;line&quot; alpha=&quot;1&quot; clip_to_extent=&quot;1&quot;>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option value=&quot;&quot; name=&quot;name&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option value=&quot;collection&quot; name=&quot;type&quot; type=&quot;QString&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;layer class=&quot;SimpleLine&quot; enabled=&quot;1&quot; pass=&quot;0&quot; locked=&quot;0&quot;>&lt;Option type=&quot;Map&quot;>&lt;Option value=&quot;0&quot; name=&quot;align_dash_pattern&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;square&quot; name=&quot;capstyle&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;5;2&quot; name=&quot;customdash&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; name=&quot;customdash_map_unit_scale&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;MM&quot; name=&quot;customdash_unit&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;0&quot; name=&quot;dash_pattern_offset&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; name=&quot;dash_pattern_offset_map_unit_scale&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;MM&quot; name=&quot;dash_pattern_offset_unit&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;0&quot; name=&quot;draw_inside_polygon&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;bevel&quot; name=&quot;joinstyle&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;60,60,60,255&quot; name=&quot;line_color&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;solid&quot; name=&quot;line_style&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;0.3&quot; name=&quot;line_width&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;MM&quot; name=&quot;line_width_unit&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;0&quot; name=&quot;offset&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; name=&quot;offset_map_unit_scale&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;MM&quot; name=&quot;offset_unit&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;0&quot; name=&quot;ring_filter&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;0&quot; name=&quot;trim_distance_end&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; name=&quot;trim_distance_end_map_unit_scale&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;MM&quot; name=&quot;trim_distance_end_unit&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;0&quot; name=&quot;trim_distance_start&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; name=&quot;trim_distance_start_map_unit_scale&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;MM&quot; name=&quot;trim_distance_start_unit&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;0&quot; name=&quot;tweak_dash_pattern_on_corners&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;0&quot; name=&quot;use_custom_dash&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; name=&quot;width_map_unit_scale&quot; type=&quot;QString&quot;/>&lt;/Option>&lt;prop k=&quot;align_dash_pattern&quot; v=&quot;0&quot;/>&lt;prop k=&quot;capstyle&quot; v=&quot;square&quot;/>&lt;prop k=&quot;customdash&quot; v=&quot;5;2&quot;/>&lt;prop k=&quot;customdash_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;customdash_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;dash_pattern_offset&quot; v=&quot;0&quot;/>&lt;prop k=&quot;dash_pattern_offset_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;dash_pattern_offset_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;draw_inside_polygon&quot; v=&quot;0&quot;/>&lt;prop k=&quot;joinstyle&quot; v=&quot;bevel&quot;/>&lt;prop k=&quot;line_color&quot; v=&quot;60,60,60,255&quot;/>&lt;prop k=&quot;line_style&quot; v=&quot;solid&quot;/>&lt;prop k=&quot;line_width&quot; v=&quot;0.3&quot;/>&lt;prop k=&quot;line_width_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;offset&quot; v=&quot;0&quot;/>&lt;prop k=&quot;offset_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;offset_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;ring_filter&quot; v=&quot;0&quot;/>&lt;prop k=&quot;trim_distance_end&quot; v=&quot;0&quot;/>&lt;prop k=&quot;trim_distance_end_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;trim_distance_end_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;trim_distance_start&quot; v=&quot;0&quot;/>&lt;prop k=&quot;trim_distance_start_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;trim_distance_start_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;tweak_dash_pattern_on_corners&quot; v=&quot;0&quot;/>&lt;prop k=&quot;use_custom_dash&quot; v=&quot;0&quot;/>&lt;prop k=&quot;width_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option value=&quot;&quot; name=&quot;name&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option value=&quot;collection&quot; name=&quot;type&quot; type=&quot;QString&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>" name="lineSymbol" type="QString"/>
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
    <DiagramCategory spacingUnit="MM" rotationOffset="270" height="15" direction="0" sizeScale="3x:0,0,0,0,0,0" spacing="5" scaleDependency="Area" scaleBasedVisibility="0" penColor="#000000" backgroundAlpha="255" maxScaleDenominator="1e+08" width="15" diagramOrientation="Up" minScaleDenominator="0" penAlpha="255" enabled="0" labelPlacementMethod="XHeight" opacity="1" penWidth="0" lineSizeScale="3x:0,0,0,0,0,0" minimumSize="0" sizeType="MM" barWidth="5" lineSizeType="MM" spacingUnitScale="3x:0,0,0,0,0,0" backgroundColor="#ffffff" showAxis="1">
      <fontProperties style="" description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0"/>
      <attribute colorOpacity="1" field="" label="" color="#000000"/>
      <axisSymbol>
        <symbol force_rhr="0" name="" type="line" alpha="1" clip_to_extent="1">
          <data_defined_properties>
            <Option type="Map">
              <Option value="" name="name" type="QString"/>
              <Option name="properties"/>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
          <layer class="SimpleLine" enabled="1" pass="0" locked="0">
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
  <DiagramLayerSettings placement="1" obstacle="0" dist="0" showAll="1" priority="0" zIndex="0" linePlacementFlags="18">
    <properties>
      <Option type="Map">
        <Option value="" name="name" type="QString"/>
        <Option name="properties"/>
        <Option value="collection" name="type" type="QString"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions removeDuplicateNodes="0" geometryPrecision="0.01">
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
    <field configurationFlags="None" name="fid">
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
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="lokalnyId">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="wersjaId">
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
    <field configurationFlags="None" name="nazwa">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="oznaczenie">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="symbol">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="poczatekWersjiObiektu">
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
    <field configurationFlags="None" name="koniecWersjiObiektu">
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
    <field configurationFlags="None" name="obowiazujeOd">
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
    <field configurationFlags="None" name="obowiazujeDo">
      <editWidget type="DateTime">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="status">
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
    <field configurationFlags="None" name="charakterUstalenia">
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
    <field configurationFlags="None" name="plan">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="wylaczenieZabudowyZagrodowej">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="odlegloscDoSzkolyPodstawowej">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="odlegloscDoObszarowZieleniPublicznej">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="powierzchniaLacznaObszarowZieleniPublicznej">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="odlegloscDoObszaruZieleniPublicznej">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="powierzchniaObszaruZieleniPublicznej">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="odlegloscDoPrzedszkola">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="odlegloscDoZlobka">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="odlegloscDoAmbulatoriumPOZ">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="odlegloscDoBiblioteki">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="odlegloscDoDomuKultury">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="odlegloscDoDomuPomocySpolecznej">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="odlegloscDoUrzadzonegoTerenuSportu">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="odlegloscDoPrzystanku">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="odlegloscDoPlacowkiPocztowej">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="odlegloscDoApteki">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="odlegloscDoPosterunkuPolicji">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="odlegloscDoPosterunkuJednostkiOchronyPrzeciwpozarowej">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias index="0" name="" field="fid"/>
    <alias index="1" name="" field="przestrzenNazw"/>
    <alias index="2" name="" field="lokalnyId"/>
    <alias index="3" name="" field="wersjaId"/>
    <alias index="4" name="" field="nazwa"/>
    <alias index="5" name="" field="oznaczenie"/>
    <alias index="6" name="" field="symbol"/>
    <alias index="7" name="" field="poczatekWersjiObiektu"/>
    <alias index="8" name="" field="koniecWersjiObiektu"/>
    <alias index="9" name="" field="obowiazujeOd"/>
    <alias index="10" name="" field="obowiazujeDo"/>
    <alias index="11" name="" field="status"/>
    <alias index="12" name="" field="charakterUstalenia"/>
    <alias index="13" name="" field="plan"/>
    <alias index="14" name="" field="wylaczenieZabudowyZagrodowej"/>
    <alias index="15" name="" field="odlegloscDoSzkolyPodstawowej"/>
    <alias index="16" name="" field="odlegloscDoObszarowZieleniPublicznej"/>
    <alias index="17" name="" field="powierzchniaLacznaObszarowZieleniPublicznej"/>
    <alias index="18" name="" field="odlegloscDoObszaruZieleniPublicznej"/>
    <alias index="19" name="" field="powierzchniaObszaruZieleniPublicznej"/>
    <alias index="20" name="" field="odlegloscDoPrzedszkola"/>
    <alias index="21" name="" field="odlegloscDoZlobka"/>
    <alias index="22" name="" field="odlegloscDoAmbulatoriumPOZ"/>
    <alias index="23" name="" field="odlegloscDoBiblioteki"/>
    <alias index="24" name="" field="odlegloscDoDomuKultury"/>
    <alias index="25" name="" field="odlegloscDoDomuPomocySpolecznej"/>
    <alias index="26" name="" field="odlegloscDoUrzadzonegoTerenuSportu"/>
    <alias index="27" name="" field="odlegloscDoPrzystanku"/>
    <alias index="28" name="" field="odlegloscDoPlacowkiPocztowej"/>
    <alias index="29" name="" field="odlegloscDoApteki"/>
    <alias index="30" name="" field="odlegloscDoPosterunkuPolicji"/>
    <alias index="31" name="" field="odlegloscDoPosterunkuJednostkiOchronyPrzeciwpozarowej"/>
  </aliases>
  <defaults>
    <default applyOnUpdate="0" field="fid" expression=""/>
    <default applyOnUpdate="0" field="przestrzenNazw" expression=""/>
    <default applyOnUpdate="0" field="lokalnyId" expression=""/>
    <default applyOnUpdate="0" field="wersjaId" expression=""/>
    <default applyOnUpdate="1" field="nazwa" expression="'Obszar standardów dostępności infrastruktury społecznej'"/>
    <default applyOnUpdate="0" field="oznaczenie" expression=""/>
    <default applyOnUpdate="0" field="symbol" expression="'OSD'"/>
    <default applyOnUpdate="0" field="poczatekWersjiObiektu" expression=""/>
    <default applyOnUpdate="0" field="koniecWersjiObiektu" expression=""/>
    <default applyOnUpdate="0" field="obowiazujeOd" expression=""/>
    <default applyOnUpdate="0" field="obowiazujeDo" expression=""/>
    <default applyOnUpdate="0" field="status" expression=""/>
    <default applyOnUpdate="0" field="charakterUstalenia" expression="'ogólnie wiążące'"/>
    <default applyOnUpdate="0" field="plan" expression=""/>
    <default applyOnUpdate="0" field="wylaczenieZabudowyZagrodowej" expression=""/>
    <default applyOnUpdate="0" field="odlegloscDoSzkolyPodstawowej" expression=""/>
    <default applyOnUpdate="0" field="odlegloscDoObszarowZieleniPublicznej" expression=""/>
    <default applyOnUpdate="0" field="powierzchniaLacznaObszarowZieleniPublicznej" expression=""/>
    <default applyOnUpdate="0" field="odlegloscDoObszaruZieleniPublicznej" expression=""/>
    <default applyOnUpdate="0" field="powierzchniaObszaruZieleniPublicznej" expression=""/>
    <default applyOnUpdate="0" field="odlegloscDoPrzedszkola" expression=""/>
    <default applyOnUpdate="0" field="odlegloscDoZlobka" expression=""/>
    <default applyOnUpdate="0" field="odlegloscDoAmbulatoriumPOZ" expression=""/>
    <default applyOnUpdate="0" field="odlegloscDoBiblioteki" expression=""/>
    <default applyOnUpdate="0" field="odlegloscDoDomuKultury" expression=""/>
    <default applyOnUpdate="0" field="odlegloscDoDomuPomocySpolecznej" expression=""/>
    <default applyOnUpdate="0" field="odlegloscDoUrzadzonegoTerenuSportu" expression=""/>
    <default applyOnUpdate="0" field="odlegloscDoPrzystanku" expression=""/>
    <default applyOnUpdate="0" field="odlegloscDoPlacowkiPocztowej" expression=""/>
    <default applyOnUpdate="0" field="odlegloscDoApteki" expression=""/>
    <default applyOnUpdate="0" field="odlegloscDoPosterunkuPolicji" expression=""/>
    <default applyOnUpdate="0" field="odlegloscDoPosterunkuJednostkiOchronyPrzeciwpozarowej" expression=""/>
  </defaults>
  <constraints>
    <constraint constraints="3" field="fid" unique_strength="1" exp_strength="0" notnull_strength="1"/>
    <constraint constraints="0" field="przestrzenNazw" unique_strength="0" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" field="lokalnyId" unique_strength="0" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" field="wersjaId" unique_strength="0" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" field="nazwa" unique_strength="0" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" field="oznaczenie" unique_strength="0" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" field="symbol" unique_strength="0" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" field="poczatekWersjiObiektu" unique_strength="0" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" field="koniecWersjiObiektu" unique_strength="0" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" field="obowiazujeOd" unique_strength="0" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" field="obowiazujeDo" unique_strength="0" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" field="status" unique_strength="0" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" field="charakterUstalenia" unique_strength="0" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" field="plan" unique_strength="0" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" field="wylaczenieZabudowyZagrodowej" unique_strength="0" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" field="odlegloscDoSzkolyPodstawowej" unique_strength="0" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" field="odlegloscDoObszarowZieleniPublicznej" unique_strength="0" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" field="powierzchniaLacznaObszarowZieleniPublicznej" unique_strength="0" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" field="odlegloscDoObszaruZieleniPublicznej" unique_strength="0" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" field="powierzchniaObszaruZieleniPublicznej" unique_strength="0" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" field="odlegloscDoPrzedszkola" unique_strength="0" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" field="odlegloscDoZlobka" unique_strength="0" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" field="odlegloscDoAmbulatoriumPOZ" unique_strength="0" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" field="odlegloscDoBiblioteki" unique_strength="0" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" field="odlegloscDoDomuKultury" unique_strength="0" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" field="odlegloscDoDomuPomocySpolecznej" unique_strength="0" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" field="odlegloscDoUrzadzonegoTerenuSportu" unique_strength="0" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" field="odlegloscDoPrzystanku" unique_strength="0" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" field="odlegloscDoPlacowkiPocztowej" unique_strength="0" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" field="odlegloscDoApteki" unique_strength="0" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" field="odlegloscDoPosterunkuPolicji" unique_strength="0" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" field="odlegloscDoPosterunkuJednostkiOchronyPrzeciwpozarowej" unique_strength="0" exp_strength="0" notnull_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="fid" exp="" desc=""/>
    <constraint field="przestrzenNazw" exp="" desc=""/>
    <constraint field="lokalnyId" exp="" desc=""/>
    <constraint field="wersjaId" exp="" desc=""/>
    <constraint field="nazwa" exp="" desc=""/>
    <constraint field="oznaczenie" exp="" desc=""/>
    <constraint field="symbol" exp="" desc=""/>
    <constraint field="poczatekWersjiObiektu" exp="" desc=""/>
    <constraint field="koniecWersjiObiektu" exp="" desc=""/>
    <constraint field="obowiazujeOd" exp="" desc=""/>
    <constraint field="obowiazujeDo" exp="" desc=""/>
    <constraint field="status" exp="" desc=""/>
    <constraint field="charakterUstalenia" exp="" desc=""/>
    <constraint field="plan" exp="" desc=""/>
    <constraint field="wylaczenieZabudowyZagrodowej" exp="" desc=""/>
    <constraint field="odlegloscDoSzkolyPodstawowej" exp="" desc=""/>
    <constraint field="odlegloscDoObszarowZieleniPublicznej" exp="" desc=""/>
    <constraint field="powierzchniaLacznaObszarowZieleniPublicznej" exp="" desc=""/>
    <constraint field="odlegloscDoObszaruZieleniPublicznej" exp="" desc=""/>
    <constraint field="powierzchniaObszaruZieleniPublicznej" exp="" desc=""/>
    <constraint field="odlegloscDoPrzedszkola" exp="" desc=""/>
    <constraint field="odlegloscDoZlobka" exp="" desc=""/>
    <constraint field="odlegloscDoAmbulatoriumPOZ" exp="" desc=""/>
    <constraint field="odlegloscDoBiblioteki" exp="" desc=""/>
    <constraint field="odlegloscDoDomuKultury" exp="" desc=""/>
    <constraint field="odlegloscDoDomuPomocySpolecznej" exp="" desc=""/>
    <constraint field="odlegloscDoUrzadzonegoTerenuSportu" exp="" desc=""/>
    <constraint field="odlegloscDoPrzystanku" exp="" desc=""/>
    <constraint field="odlegloscDoPlacowkiPocztowej" exp="" desc=""/>
    <constraint field="odlegloscDoApteki" exp="" desc=""/>
    <constraint field="odlegloscDoPosterunkuPolicji" exp="" desc=""/>
    <constraint field="odlegloscDoPosterunkuJednostkiOchronyPrzeciwpozarowej" exp="" desc=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig sortExpression="" actionWidgetStyle="dropDown" sortOrder="0">
    <columns>
      <column name="przestrzenNazw" width="-1" type="field" hidden="0"/>
      <column name="lokalnyId" width="-1" type="field" hidden="0"/>
      <column name="wersjaId" width="-1" type="field" hidden="0"/>
      <column name="poczatekWersjiObiektu" width="-1" type="field" hidden="0"/>
      <column name="koniecWersjiObiektu" width="-1" type="field" hidden="0"/>
      <column name="obowiazujeOd" width="-1" type="field" hidden="0"/>
      <column name="obowiazujeDo" width="-1" type="field" hidden="0"/>
      <column name="nazwa" width="-1" type="field" hidden="0"/>
      <column name="oznaczenie" width="-1" type="field" hidden="0"/>
      <column name="symbol" width="-1" type="field" hidden="0"/>
      <column name="charakterUstalenia" width="-1" type="field" hidden="0"/>
      <column name="plan" width="-1" type="field" hidden="0"/>
      <column name="wylaczenieZabudowyZagrodowej" width="199" type="field" hidden="0"/>
      <column name="fid" width="-1" type="field" hidden="0"/>
      <column name="status" width="-1" type="field" hidden="0"/>
      <column name="odlegloscDoSzkolyPodstawowej" width="-1" type="field" hidden="0"/>
      <column name="odlegloscDoObszarowZieleniPublicznej" width="-1" type="field" hidden="0"/>
      <column name="odlegloscDoObszaruZieleniPublicznej" width="-1" type="field" hidden="0"/>
      <column name="odlegloscDoPrzedszkola" width="-1" type="field" hidden="0"/>
      <column name="odlegloscDoZlobka" width="-1" type="field" hidden="0"/>
      <column name="odlegloscDoAmbulatoriumPOZ" width="-1" type="field" hidden="0"/>
      <column name="odlegloscDoBiblioteki" width="-1" type="field" hidden="0"/>
      <column name="odlegloscDoDomuKultury" width="-1" type="field" hidden="0"/>
      <column name="odlegloscDoDomuPomocySpolecznej" width="-1" type="field" hidden="0"/>
      <column name="odlegloscDoUrzadzonegoTerenuSportu" width="-1" type="field" hidden="0"/>
      <column name="odlegloscDoPrzystanku" width="-1" type="field" hidden="0"/>
      <column name="odlegloscDoPlacowkiPocztowej" width="-1" type="field" hidden="0"/>
      <column name="odlegloscDoApteki" width="-1" type="field" hidden="0"/>
      <column name="odlegloscDoPosterunkuPolicji" width="-1" type="field" hidden="0"/>
      <column name="odlegloscDoPosterunkuJednostkiOchronyPrzeciwpozarowej" width="-1" type="field" hidden="0"/>
      <column name="powierzchniaLacznaObszarowZieleniPublicznej" width="-1" type="field" hidden="0"/>
      <column name="powierzchniaObszaruZieleniPublicznej" width="-1" type="field" hidden="0"/>
      <column width="-1" type="actions" hidden="1"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <storedexpressions/>
  <editform tolerant="1">C:\Users\mlebiecki\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\wtyczka_qgis_app\ObszarStandardowDostepnosciInfrastrukturySpolecznej.ui</editform>
  <editforminit>my_form_open</editforminit>
  <editforminitcodesource>1</editforminitcodesource>
  <editforminitfilepath>C:\Users\mlebiecki\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\wtyczka_qgis_app\ObszarStandardowDostepnosciInfrastrukturySpolecznej.py</editforminitfilepath>
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
    <field editable="1" name="charakterUstalenia"/>
    <field editable="1" name="fid"/>
    <field editable="1" name="gml_id"/>
    <field editable="1" name="koniecWersjiObiektu"/>
    <field editable="1" name="lokalnyId"/>
    <field editable="0" name="nazwa"/>
    <field editable="1" name="obowiazujeDo"/>
    <field editable="1" name="obowiazujeOd"/>
    <field editable="1" name="odlegloscDoAmbulatoriumPOZ"/>
    <field editable="1" name="odlegloscDoApteki"/>
    <field editable="1" name="odlegloscDoBiblioteki"/>
    <field editable="1" name="odlegloscDoDomuKultury"/>
    <field editable="1" name="odlegloscDoDomuPomocySpolecznej"/>
    <field editable="1" name="odlegloscDoObszarowZieleniPublicznej"/>
    <field editable="1" name="odlegloscDoObszaruZieleniPublicznej"/>
    <field editable="1" name="odlegloscDoPlacowkiPocztowej"/>
    <field editable="1" name="odlegloscDoPosterunkuJednostkiOchronyPrzeciwpozarowej"/>
    <field editable="1" name="odlegloscDoPosterunkuPolicji"/>
    <field editable="1" name="odlegloscDoPrzedszkola"/>
    <field editable="1" name="odlegloscDoPrzystanku"/>
    <field editable="1" name="odlegloscDoSzkolyPodstawowej"/>
    <field editable="1" name="odlegloscDoUrzadzonegoTerenuSportu"/>
    <field editable="1" name="odlegloscDoZlobka"/>
    <field editable="1" name="oznaczenie"/>
    <field editable="1" name="plan"/>
    <field editable="1" name="poczatekWersjiObiektu"/>
    <field editable="1" name="powierzchniaLacznaObszarowZieleniPublicznej"/>
    <field editable="1" name="powierzchniaObszaruZieleniPublicznej"/>
    <field editable="1" name="przestrzenNazw"/>
    <field editable="1" name="status"/>
    <field editable="0" name="symbol"/>
    <field editable="1" name="tytul"/>
    <field editable="1" name="wersjaId"/>
    <field editable="1" name="wylaczenieZabudowyZagrodowej"/>
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

<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis styleCategories="Symbology|Symbology3D|Labeling|Fields|Forms|Actions|MapTips|Diagrams|AttributeTable|Rendering|CustomProperties|GeometryOptions|Relations|Temporal|Legend|Elevation|Notes" simplifyAlgorithm="0" symbologyReferenceScale="-1" version="3.22.15-Białowieża" simplifyDrawingHints="0" simplifyDrawingTol="2" labelsEnabled="0" minScale="100000000" hasScaleBasedVisibilityFlag="0" simplifyMaxScale="1" simplifyLocal="1" maxScale="0">
  <temporal durationField="" limitMode="0" endExpression="" durationUnit="min" startField="" mode="0" enabled="0" startExpression="" endField="" fixedDuration="0" accumulate="0">
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
            <Option value="14;10" name="customdash" type="QString"/>
            <Option value="3x:0,0,0,0,0,0" name="customdash_map_unit_scale" type="QString"/>
            <Option value="MM" name="customdash_unit" type="QString"/>
            <Option value="0" name="dash_pattern_offset" type="QString"/>
            <Option value="3x:0,0,0,0,0,0" name="dash_pattern_offset_map_unit_scale" type="QString"/>
            <Option value="MM" name="dash_pattern_offset_unit" type="QString"/>
            <Option value="0" name="draw_inside_polygon" type="QString"/>
            <Option value="miter" name="joinstyle" type="QString"/>
            <Option value="83,83,83,255" name="line_color" type="QString"/>
            <Option value="dash" name="line_style" type="QString"/>
            <Option value="3" name="line_width" type="QString"/>
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
          <prop k="customdash" v="14;10"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="dash_pattern_offset" v="0"/>
          <prop k="dash_pattern_offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="dash_pattern_offset_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="miter"/>
          <prop k="line_color" v="83,83,83,255"/>
          <prop k="line_style" v="dash"/>
          <prop k="line_width" v="3"/>
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
                  <Option value="if(@map_scale&lt;=10000,3,1.5)" name="expression" type="QString"/>
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
  <customproperties>
    <Option type="Map">
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
    <field configurationFlags="None" name="tytul">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="tytulAlternatywny">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="typPlanu">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option value="plan ogólny gminy" name="plan ogólny gminy" type="QString"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="poziomHierarchii">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option value="lokalny" name="lokalny" type="QString"/>
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
    <field configurationFlags="None" name="modyfikacja">
      <editWidget type="CheckBox">
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
    <alias index="4" name="" field="poczatekWersjiObiektu"/>
    <alias index="5" name="" field="koniecWersjiObiektu"/>
    <alias index="6" name="" field="tytul"/>
    <alias index="7" name="" field="tytulAlternatywny"/>
    <alias index="8" name="" field="typPlanu"/>
    <alias index="9" name="" field="poziomHierarchii"/>
    <alias index="10" name="" field="obowiazujeOd"/>
    <alias index="11" name="" field="obowiazujeDo"/>
    <alias index="12" name="" field="status"/>
    <alias index="13" name="" field="modyfikacja"/>
  </aliases>
  <defaults>
    <default applyOnUpdate="0" field="fid" expression=""/>
    <default applyOnUpdate="0" field="przestrzenNazw" expression=""/>
    <default applyOnUpdate="0" field="lokalnyId" expression=""/>
    <default applyOnUpdate="0" field="wersjaId" expression=""/>
    <default applyOnUpdate="0" field="poczatekWersjiObiektu" expression=""/>
    <default applyOnUpdate="0" field="koniecWersjiObiektu" expression=""/>
    <default applyOnUpdate="0" field="tytul" expression=""/>
    <default applyOnUpdate="0" field="tytulAlternatywny" expression=""/>
    <default applyOnUpdate="1" field="typPlanu" expression="'plan ogólny gminy'"/>
    <default applyOnUpdate="1" field="poziomHierarchii" expression="'lokalny'"/>
    <default applyOnUpdate="0" field="obowiazujeOd" expression=""/>
    <default applyOnUpdate="0" field="obowiazujeDo" expression=""/>
    <default applyOnUpdate="0" field="status" expression=""/>
    <default applyOnUpdate="0" field="modyfikacja" expression=""/>
  </defaults>
  <constraints>
    <constraint constraints="3" field="fid" unique_strength="1" exp_strength="0" notnull_strength="1"/>
    <constraint constraints="0" field="przestrzenNazw" unique_strength="0" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" field="lokalnyId" unique_strength="0" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" field="wersjaId" unique_strength="0" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" field="poczatekWersjiObiektu" unique_strength="0" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" field="koniecWersjiObiektu" unique_strength="0" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" field="tytul" unique_strength="0" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" field="tytulAlternatywny" unique_strength="0" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" field="typPlanu" unique_strength="0" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" field="poziomHierarchii" unique_strength="0" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" field="obowiazujeOd" unique_strength="0" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" field="obowiazujeDo" unique_strength="0" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" field="status" unique_strength="0" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" field="modyfikacja" unique_strength="0" exp_strength="0" notnull_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="fid" exp="" desc=""/>
    <constraint field="przestrzenNazw" exp="" desc=""/>
    <constraint field="lokalnyId" exp="" desc=""/>
    <constraint field="wersjaId" exp="" desc=""/>
    <constraint field="poczatekWersjiObiektu" exp="" desc=""/>
    <constraint field="koniecWersjiObiektu" exp="" desc=""/>
    <constraint field="tytul" exp="" desc=""/>
    <constraint field="tytulAlternatywny" exp="" desc=""/>
    <constraint field="typPlanu" exp="" desc=""/>
    <constraint field="poziomHierarchii" exp="" desc=""/>
    <constraint field="obowiazujeOd" exp="" desc=""/>
    <constraint field="obowiazujeDo" exp="" desc=""/>
    <constraint field="status" exp="" desc=""/>
    <constraint field="modyfikacja" exp="" desc=""/>
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
      <column name="poczatekWersjiObiektu" width="178" type="field" hidden="0"/>
      <column name="koniecWersjiObiektu" width="-1" type="field" hidden="0"/>
      <column name="tytul" width="-1" type="field" hidden="0"/>
      <column name="obowiazujeOd" width="-1" type="field" hidden="0"/>
      <column name="obowiazujeDo" width="-1" type="field" hidden="0"/>
      <column name="tytulAlternatywny" width="-1" type="field" hidden="0"/>
      <column name="typPlanu" width="-1" type="field" hidden="0"/>
      <column name="poziomHierarchii" width="-1" type="field" hidden="0"/>
      <column name="status" width="-1" type="field" hidden="0"/>
      <column name="fid" width="-1" type="field" hidden="0"/>
      <column name="modyfikacja" width="-1" type="field" hidden="0"/>
      <column width="-1" type="actions" hidden="1"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <storedexpressions/>
  <editform tolerant="1">C:\Users\mlebiecki\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\wtyczka_qgis_app\AktPlanowaniaPrzestrzennego.ui</editform>
  <editforminit>my_form_open</editforminit>
  <editforminitcodesource>1</editforminitcodesource>
  <editforminitfilepath>C:\Users\mlebiecki\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\wtyczka_qgis_app\AktPlanowaniaPrzestrzennego.py</editforminitfilepath>
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
    <field editable="1" name="fid"/>
    <field editable="1" name="gml_id"/>
    <field editable="1" name="koniecWersjiObiektu"/>
    <field editable="1" name="lokalnyId"/>
    <field editable="1" name="modyfikacja"/>
    <field editable="1" name="obowiazujeDo"/>
    <field editable="1" name="obowiazujeOd"/>
    <field editable="1" name="poczatekWersjiObiektu"/>
    <field editable="1" name="poziomHierarchii"/>
    <field editable="1" name="przestrzenNazw"/>
    <field editable="1" name="status"/>
    <field editable="1" name="typPlanu"/>
    <field editable="1" name="tytul"/>
    <field editable="1" name="tytulAlternatywny"/>
    <field editable="1" name="wersjaId"/>
  </editable>
  <labelOnTop>
    <field name="fid" labelOnTop="0"/>
    <field name="gml_id" labelOnTop="0"/>
    <field name="koniecWersjiObiektu" labelOnTop="0"/>
    <field name="lokalnyId" labelOnTop="0"/>
    <field name="modyfikacja" labelOnTop="0"/>
    <field name="obowiazujeDo" labelOnTop="0"/>
    <field name="obowiazujeOd" labelOnTop="0"/>
    <field name="poczatekWersjiObiektu" labelOnTop="0"/>
    <field name="poziomHierarchii" labelOnTop="0"/>
    <field name="przestrzenNazw" labelOnTop="0"/>
    <field name="status" labelOnTop="0"/>
    <field name="typPlanu" labelOnTop="0"/>
    <field name="tytul" labelOnTop="0"/>
    <field name="tytulAlternatywny" labelOnTop="0"/>
    <field name="wersjaId" labelOnTop="0"/>
  </labelOnTop>
  <reuseLastValue>
    <field name="fid" reuseLastValue="0"/>
    <field name="gml_id" reuseLastValue="0"/>
    <field name="koniecWersjiObiektu" reuseLastValue="0"/>
    <field name="lokalnyId" reuseLastValue="0"/>
    <field name="modyfikacja" reuseLastValue="0"/>
    <field name="obowiazujeDo" reuseLastValue="0"/>
    <field name="obowiazujeOd" reuseLastValue="0"/>
    <field name="poczatekWersjiObiektu" reuseLastValue="0"/>
    <field name="poziomHierarchii" reuseLastValue="0"/>
    <field name="przestrzenNazw" reuseLastValue="0"/>
    <field name="status" reuseLastValue="0"/>
    <field name="typPlanu" reuseLastValue="0"/>
    <field name="tytul" reuseLastValue="0"/>
    <field name="tytulAlternatywny" reuseLastValue="0"/>
    <field name="wersjaId" reuseLastValue="0"/>
  </reuseLastValue>
  <dataDefinedFieldProperties/>
  <widgets/>
  <mapTip></mapTip>
  <layerGeometryType>2</layerGeometryType>
</qgis>

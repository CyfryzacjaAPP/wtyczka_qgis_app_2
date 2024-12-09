<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis symbologyReferenceScale="-1" simplifyDrawingHints="0" styleCategories="Symbology|Symbology3D|Labeling|Fields|Forms|Actions|MapTips|Diagrams|AttributeTable|Rendering|CustomProperties|GeometryOptions|Relations|Temporal|Legend|Elevation|Notes" simplifyLocal="1" hasScaleBasedVisibilityFlag="0" simplifyMaxScale="1" version="3.22.15-Białowieża" labelsEnabled="0" simplifyDrawingTol="2" maxScale="0" minScale="100000000" simplifyAlgorithm="0">
  <temporal durationUnit="min" enabled="0" startField="" endExpression="" accumulate="0" startExpression="" endField="" durationField="" mode="0" limitMode="0" fixedDuration="0">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <renderer-v2 type="singleSymbol" forceraster="0" symbollevels="0" referencescale="-1" enableorderby="0">
    <symbols>
      <symbol type="fill" force_rhr="0" name="0" clip_to_extent="1" alpha="1">
        <data_defined_properties>
          <Option type="Map">
            <Option type="QString" name="name" value=""/>
            <Option name="properties"/>
            <Option type="QString" name="type" value="collection"/>
          </Option>
        </data_defined_properties>
        <layer enabled="1" locked="0" pass="0" class="SimpleLine">
          <Option type="Map">
            <Option type="QString" name="align_dash_pattern" value="0"/>
            <Option type="QString" name="capstyle" value="flat"/>
            <Option type="QString" name="customdash" value="14;10"/>
            <Option type="QString" name="customdash_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="customdash_unit" value="MM"/>
            <Option type="QString" name="dash_pattern_offset" value="0"/>
            <Option type="QString" name="dash_pattern_offset_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="dash_pattern_offset_unit" value="MM"/>
            <Option type="QString" name="draw_inside_polygon" value="0"/>
            <Option type="QString" name="joinstyle" value="miter"/>
            <Option type="QString" name="line_color" value="83,83,83,255"/>
            <Option type="QString" name="line_style" value="dash"/>
            <Option type="QString" name="line_width" value="3"/>
            <Option type="QString" name="line_width_unit" value="MM"/>
            <Option type="QString" name="offset" value="0"/>
            <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="offset_unit" value="MM"/>
            <Option type="QString" name="ring_filter" value="0"/>
            <Option type="QString" name="trim_distance_end" value="0"/>
            <Option type="QString" name="trim_distance_end_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="trim_distance_end_unit" value="MM"/>
            <Option type="QString" name="trim_distance_start" value="0"/>
            <Option type="QString" name="trim_distance_start_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="trim_distance_start_unit" value="MM"/>
            <Option type="QString" name="tweak_dash_pattern_on_corners" value="0"/>
            <Option type="QString" name="use_custom_dash" value="1"/>
            <Option type="QString" name="width_map_unit_scale" value="3x:0,0,0,0,0,0"/>
          </Option>
          <prop v="0" k="align_dash_pattern"/>
          <prop v="flat" k="capstyle"/>
          <prop v="14;10" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="dash_pattern_offset"/>
          <prop v="3x:0,0,0,0,0,0" k="dash_pattern_offset_map_unit_scale"/>
          <prop v="MM" k="dash_pattern_offset_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="miter" k="joinstyle"/>
          <prop v="83,83,83,255" k="line_color"/>
          <prop v="dash" k="line_style"/>
          <prop v="3" k="line_width"/>
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
              <Option type="QString" name="name" value=""/>
              <Option type="Map" name="properties">
                <Option type="Map" name="customDash">
                  <Option type="bool" name="active" value="true"/>
                  <Option type="QString" name="expression" value="if(@map_scale&lt;=10000,'14;10','7;5')"/>
                  <Option type="int" name="type" value="3"/>
                </Option>
                <Option type="Map" name="outlineWidth">
                  <Option type="bool" name="active" value="true"/>
                  <Option type="QString" name="expression" value="if(@map_scale&lt;=10000,3,1.5)"/>
                  <Option type="int" name="type" value="3"/>
                </Option>
              </Option>
              <Option type="QString" name="type" value="collection"/>
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
      <Option type="int" name="embeddedWidgets/count" value="0"/>
      <Option name="variableNames"/>
      <Option name="variableValues"/>
    </Option>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Histogram">
    <DiagramCategory maxScaleDenominator="1e+08" labelPlacementMethod="XHeight" showAxis="1" diagramOrientation="Up" scaleBasedVisibility="0" sizeScale="3x:0,0,0,0,0,0" penWidth="0" penAlpha="255" minScaleDenominator="0" penColor="#000000" backgroundColor="#ffffff" scaleDependency="Area" barWidth="5" minimumSize="0" direction="0" lineSizeType="MM" height="15" enabled="0" sizeType="MM" width="15" rotationOffset="270" spacingUnit="MM" opacity="1" spacingUnitScale="3x:0,0,0,0,0,0" spacing="5" lineSizeScale="3x:0,0,0,0,0,0" backgroundAlpha="255">
      <fontProperties style="" description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0"/>
      <attribute colorOpacity="1" color="#000000" field="" label=""/>
      <axisSymbol>
        <symbol type="line" force_rhr="0" name="" clip_to_extent="1" alpha="1">
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option name="properties"/>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
          <layer enabled="1" locked="0" pass="0" class="SimpleLine">
            <Option type="Map">
              <Option type="QString" name="align_dash_pattern" value="0"/>
              <Option type="QString" name="capstyle" value="square"/>
              <Option type="QString" name="customdash" value="5;2"/>
              <Option type="QString" name="customdash_map_unit_scale" value="3x:0,0,0,0,0,0"/>
              <Option type="QString" name="customdash_unit" value="MM"/>
              <Option type="QString" name="dash_pattern_offset" value="0"/>
              <Option type="QString" name="dash_pattern_offset_map_unit_scale" value="3x:0,0,0,0,0,0"/>
              <Option type="QString" name="dash_pattern_offset_unit" value="MM"/>
              <Option type="QString" name="draw_inside_polygon" value="0"/>
              <Option type="QString" name="joinstyle" value="bevel"/>
              <Option type="QString" name="line_color" value="35,35,35,255"/>
              <Option type="QString" name="line_style" value="solid"/>
              <Option type="QString" name="line_width" value="0.26"/>
              <Option type="QString" name="line_width_unit" value="MM"/>
              <Option type="QString" name="offset" value="0"/>
              <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0"/>
              <Option type="QString" name="offset_unit" value="MM"/>
              <Option type="QString" name="ring_filter" value="0"/>
              <Option type="QString" name="trim_distance_end" value="0"/>
              <Option type="QString" name="trim_distance_end_map_unit_scale" value="3x:0,0,0,0,0,0"/>
              <Option type="QString" name="trim_distance_end_unit" value="MM"/>
              <Option type="QString" name="trim_distance_start" value="0"/>
              <Option type="QString" name="trim_distance_start_map_unit_scale" value="3x:0,0,0,0,0,0"/>
              <Option type="QString" name="trim_distance_start_unit" value="MM"/>
              <Option type="QString" name="tweak_dash_pattern_on_corners" value="0"/>
              <Option type="QString" name="use_custom_dash" value="0"/>
              <Option type="QString" name="width_map_unit_scale" value="3x:0,0,0,0,0,0"/>
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
                <Option type="QString" name="name" value=""/>
                <Option name="properties"/>
                <Option type="QString" name="type" value="collection"/>
              </Option>
            </data_defined_properties>
          </layer>
        </symbol>
      </axisSymbol>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings showAll="1" linePlacementFlags="18" placement="1" zIndex="0" priority="0" obstacle="0" dist="0">
    <properties>
      <Option type="Map">
        <Option type="QString" name="name" value=""/>
        <Option name="properties"/>
        <Option type="QString" name="type" value="collection"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions removeDuplicateNodes="0">
    <activeChecks/>
    <checkConfiguration type="Map">
      <Option type="Map" name="QgsGeometryGapCheck">
        <Option type="double" name="allowedGapsBuffer" value="0"/>
        <Option type="bool" name="allowedGapsEnabled" value="false"/>
        <Option type="QString" name="allowedGapsLayer" value=""/>
      </Option>
    </checkConfiguration>
  </geometryOptions>
  <legend type="default-vector" showLabelLegend="0"/>
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
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="lokalnyId" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="wersjaId" configurationFlags="None">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option type="bool" name="allow_null" value="true"/>
            <Option type="bool" name="calendar_popup" value="true"/>
            <Option type="QString" name="display_format" value="yyyyMMddTHHmmss"/>
            <Option type="QString" name="field_format" value="yyyyMMddTHHmmss"/>
            <Option type="bool" name="field_iso_format" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="poczatekWersjiObiektu" configurationFlags="None">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option type="bool" name="allow_null" value="true"/>
            <Option type="bool" name="calendar_popup" value="true"/>
            <Option type="QString" name="display_format" value="yyyy-MM-ddTHH:mm:ssZ"/>
            <Option type="QString" name="field_format" value="yyyy-MM-ddTHH:mm:ssZ"/>
            <Option type="bool" name="field_iso_format" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="koniecWersjiObiektu" configurationFlags="None">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option type="bool" name="allow_null" value="true"/>
            <Option type="bool" name="calendar_popup" value="true"/>
            <Option type="QString" name="display_format" value="yyyy-MM-ddTHH:mm:ssZ"/>
            <Option type="QString" name="field_format" value="yyyy-MM-ddTHH:mm:ssZ"/>
            <Option type="bool" name="field_iso_format" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="tytul" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="tytulAlternatywny" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="typPlanu" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option type="QString" name="plan ogólny gminy" value="plan ogólny gminy"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="poziomHierarchii" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option type="QString" name="lokalny" value="lokalny"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="obowiazujeOd" configurationFlags="None">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option type="bool" name="allow_null" value="true"/>
            <Option type="bool" name="calendar_popup" value="true"/>
            <Option type="QString" name="display_format" value="yyyy-MM-dd"/>
            <Option type="QString" name="field_format" value="yyyy-MM-dd"/>
            <Option type="bool" name="field_iso_format" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="obowiazujeDo" configurationFlags="None">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option type="bool" name="allow_null" value="true"/>
            <Option type="bool" name="calendar_popup" value="true"/>
            <Option type="QString" name="display_format" value="yyyy-MM-dd"/>
            <Option type="QString" name="field_format" value="yyyy-MM-dd"/>
            <Option type="bool" name="field_iso_format" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="status" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option type="QString" name="nieaktualny" value="nieaktualny"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="prawnie wiążący lub realizowany" value="prawnie wiążący lub realizowany"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="w opracowaniu" value="w opracowaniu"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="w trakcie przyjmowania" value="w trakcie przyjmowania"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="wybierz" value="{2839923C-8B7D-419E-B84B-CA2FE9B80EC7}"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="modyfikacja" configurationFlags="None">
      <editWidget type="CheckBox">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias field="fid" index="0" name=""/>
    <alias field="przestrzenNazw" index="1" name=""/>
    <alias field="lokalnyId" index="2" name=""/>
    <alias field="wersjaId" index="3" name=""/>
    <alias field="poczatekWersjiObiektu" index="4" name=""/>
    <alias field="koniecWersjiObiektu" index="5" name=""/>
    <alias field="tytul" index="6" name=""/>
    <alias field="tytulAlternatywny" index="7" name=""/>
    <alias field="typPlanu" index="8" name=""/>
    <alias field="poziomHierarchii" index="9" name=""/>
    <alias field="obowiazujeOd" index="10" name=""/>
    <alias field="obowiazujeDo" index="11" name=""/>
    <alias field="status" index="12" name=""/>
    <alias field="modyfikacja" index="13" name=""/>
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
    <constraint constraints="3" exp_strength="0" field="fid" unique_strength="1" notnull_strength="1"/>
    <constraint constraints="0" exp_strength="0" field="przestrzenNazw" unique_strength="0" notnull_strength="0"/>
    <constraint constraints="0" exp_strength="0" field="lokalnyId" unique_strength="0" notnull_strength="0"/>
    <constraint constraints="0" exp_strength="0" field="wersjaId" unique_strength="0" notnull_strength="0"/>
    <constraint constraints="0" exp_strength="0" field="poczatekWersjiObiektu" unique_strength="0" notnull_strength="0"/>
    <constraint constraints="0" exp_strength="0" field="koniecWersjiObiektu" unique_strength="0" notnull_strength="0"/>
    <constraint constraints="0" exp_strength="0" field="tytul" unique_strength="0" notnull_strength="0"/>
    <constraint constraints="0" exp_strength="0" field="tytulAlternatywny" unique_strength="0" notnull_strength="0"/>
    <constraint constraints="0" exp_strength="0" field="typPlanu" unique_strength="0" notnull_strength="0"/>
    <constraint constraints="0" exp_strength="0" field="poziomHierarchii" unique_strength="0" notnull_strength="0"/>
    <constraint constraints="0" exp_strength="0" field="obowiazujeOd" unique_strength="0" notnull_strength="0"/>
    <constraint constraints="0" exp_strength="0" field="obowiazujeDo" unique_strength="0" notnull_strength="0"/>
    <constraint constraints="0" exp_strength="0" field="status" unique_strength="0" notnull_strength="0"/>
    <constraint constraints="0" exp_strength="0" field="modyfikacja" unique_strength="0" notnull_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="fid" desc="" exp=""/>
    <constraint field="przestrzenNazw" desc="" exp=""/>
    <constraint field="lokalnyId" desc="" exp=""/>
    <constraint field="wersjaId" desc="" exp=""/>
    <constraint field="poczatekWersjiObiektu" desc="" exp=""/>
    <constraint field="koniecWersjiObiektu" desc="" exp=""/>
    <constraint field="tytul" desc="" exp=""/>
    <constraint field="tytulAlternatywny" desc="" exp=""/>
    <constraint field="typPlanu" desc="" exp=""/>
    <constraint field="poziomHierarchii" desc="" exp=""/>
    <constraint field="obowiazujeOd" desc="" exp=""/>
    <constraint field="obowiazujeDo" desc="" exp=""/>
    <constraint field="status" desc="" exp=""/>
    <constraint field="modyfikacja" desc="" exp=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig sortExpression="" actionWidgetStyle="dropDown" sortOrder="0">
    <columns>
      <column type="field" name="fid" hidden="0" width="-1"/>
      <column type="field" name="przestrzenNazw" hidden="0" width="-1"/>
      <column type="field" name="lokalnyId" hidden="0" width="-1"/>
      <column type="field" name="wersjaId" hidden="0" width="-1"/>
      <column type="field" name="poczatekWersjiObiektu" hidden="0" width="178"/>
      <column type="field" name="koniecWersjiObiektu" hidden="0" width="-1"/>
      <column type="field" name="tytul" hidden="0" width="-1"/>
      <column type="field" name="tytulAlternatywny" hidden="0" width="-1"/>
      <column type="field" name="typPlanu" hidden="0" width="-1"/>
      <column type="field" name="poziomHierarchii" hidden="0" width="-1"/>
      <column type="field" name="obowiazujeOd" hidden="0" width="-1"/>
      <column type="field" name="obowiazujeDo" hidden="0" width="-1"/>
      <column type="field" name="status" hidden="0" width="-1"/>
      <column type="field" name="modyfikacja" hidden="0" width="-1"/>
      <column type="actions" hidden="1" width="-1"/>
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
    <field labelOnTop="0" name="fid"/>
    <field labelOnTop="0" name="gml_id"/>
    <field labelOnTop="0" name="koniecWersjiObiektu"/>
    <field labelOnTop="0" name="lokalnyId"/>
    <field labelOnTop="0" name="modyfikacja"/>
    <field labelOnTop="0" name="obowiazujeDo"/>
    <field labelOnTop="0" name="obowiazujeOd"/>
    <field labelOnTop="0" name="poczatekWersjiObiektu"/>
    <field labelOnTop="0" name="poziomHierarchii"/>
    <field labelOnTop="0" name="przestrzenNazw"/>
    <field labelOnTop="0" name="status"/>
    <field labelOnTop="0" name="typPlanu"/>
    <field labelOnTop="0" name="tytul"/>
    <field labelOnTop="0" name="tytulAlternatywny"/>
    <field labelOnTop="0" name="wersjaId"/>
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

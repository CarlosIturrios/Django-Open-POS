from django.db.models import Q
from rest_framework import serializers

from catalogos.models import Clase
from catalogos.models import ConceptoDeIngreso
from catalogos.models import Rubro
from catalogos.models import Tipo
from opensir.mixins import CustomModelSerializerMixin


class RubroSerializer(serializers.ModelSerializer):
    """
        Serializer rubro para crear, listar y modificar un rubro
    """

    class Meta:
        model = Rubro
        fields = (
            'id',
            'clave',
            'denominacion',
            'nivel',
            'estados_globales'
        )
        read_only_fields = (
            'id',
            'clave',
            'denominacion',
            'nivel',
        )

    def validate_clave(self, valor):
        """Validaciones para clave

        Validaciones:
        - Debe ser único
        """
        exists = self.model.objects.filter(
            ~Q(id=self.instance.id if self.instance is not None else None),
            clave=valor,
        ).exists()
        if exists:
            raise serializers.ValidationError('La clave debe ser única.')
        return valor.upper()


class TipoSerializer(serializers.ModelSerializer):
    """
        Serializer Tipo con relacion a rubro para crear, listar y modificar un tipo
    """

    class Meta:
        model = Tipo
        fields = (
            'id',
            'clave',
            'denominacion',
            'nivel',
            'estados_globales'
        )
        read_only_fields = (
            'id',
            'clave',
            'denominacion',
            'nivel',
        )

    def validate_clave(self, valor):
        """Validaciones para clave

        Validaciones:
        - Debe ser único
        """
        exists = self.model.objects.filter(
            ~Q(id=self.instance.id if self.instance is not None else None),
            clave=valor,
        ).exists()
        if exists:
            raise serializers.ValidationError('La clave debe ser única.')
        return valor.upper()


class RubroTiposSerializer(CustomModelSerializerMixin):
    tipos = TipoSerializer(source='relacion_rubro_a_tipo', many=True)

    class Meta:
        model = Rubro
        fields = [
            'id',
            'clave',
            'denominacion',
            'nivel',
            'tipos',
            'estados_globales'
        ]
        read_only_fields = fields

    def validate_clave(self, valor):
        """Validaciones para clave

        Validaciones:
        - Debe ser único
        """
        exists = self.model.objects.filter(
            ~Q(id=self.instance.id if self.instance is not None else None),
            clave=valor,
        ).exists()
        if exists:
            raise serializers.ValidationError('La clave debe ser única.')
        return valor.upper()


class ClaseSerializer(CustomModelSerializerMixin):
    """
        Serializer Clase con relacion a Tipo para crear, listar y modificar una clase
    """

    class Meta:
        model = Clase
        fields = (
            'id',
            'clave',
            'denominacion',
            'nivel',
            'tipo',
            'estados_globales'
        )
        read_only_fields = (
            'id',
            'nivel',
        )

    def validate_clave(self, valor):
        """Validaciones para clave

        Validaciones:
        - Debe ser único
        """
        exists = self.model.objects.filter(
            ~Q(id=self.instance.id if self.instance is not None else None),
            clave=valor,
        ).exists()
        if exists:
            raise serializers.ValidationError('La clave debe ser única.')
        return valor.upper()

    def validate_tipo(self, tipo):
        """Validaciones para tipo

        Validaciones:
        - Relacional
        """
        return self.validacion_relacional(tipo, 'Tipo no válido')

    def create(self, validated_data):
        clase = super().create(validated_data)
        clase.nivel = 3

        return clase


class ConceptoDeIngresoSerializer(CustomModelSerializerMixin):
    """Serializer para el modelo presupuesto de ingreso.

    Maneja la lógica de las operaciones CRUD.

    Se espera que la la vista que implemente este endpoint tenga
    valide que el usuario tenga asignado un canal de pago.
    """

    class Meta:
        model = ConceptoDeIngreso
        fields = [
            'id',
            'clave',
            'descripcion',
            'sub_cuenta_contable',
            'es_ingreso_presupuestal',
            'tipos_de_recargo',
            'tipos_de_actualizacion',
            'tipos_de_descuento',
            'naturaleza_de_ingresos',
            'fundamento_legal',
            'fuente_de_ingreso',
            'clasificador_economico',
            'periodo_fiscal',
            'padron',
            'canales_de_pago',
            'cri_clase',
            'estados_globales',
        ]
        read_only_fields = ('id', 'canales_de_pago',)

    def validate_clave(self, valor):
        """Validaciones para clave

        Validaciones:
        - Debe ser único
        """
        exists = self.model.objects.filter(
            ~Q(id=self.instance.id if self.instance is not None else None),
            clave=valor,
        ).exists()
        if exists:
            raise serializers.ValidationError('La clave debe ser única.')
        return valor.upper()

    def validate_descripcion(self, valor):
        """Normalización de descripcion.

        Formatos:
        - Capitalización.
        """
        return valor.capitalize()

    def validate_sub_cuenta_contable(self, valor):
        """Validación de sub cuenta contable.

        Validaciones:
        - Número positivo
        """
        return self.validacion_numeros_positivos(valor, 'Sub cuenta contable no válida.')

    def validate_tipos_de_recargo(self, tipos_de_recargo):
        """Validaciones para tipos de recargo.

        Validaciones:
        - Relacional
        """
        return self.validacion_relacional(tipos_de_recargo, 'Tipos de recargo no válidos.')

    def validate_tipos_de_actualizacion(self, tipos_de_actualizacion):
        """Validaciones para tipo Tipos de actualizacion

        Validaciones:
        - Relacional
        """
        return self.validacion_relacional(tipos_de_actualizacion, 'Tipos de actualización no válidas.')

    def validate_tipos_de_descuento(self, tipos_de_descuento):
        """Validaciones para tipo Tipos de descuento

        Validaciones:
        - Relacional
        """
        return self.validacion_relacional(tipos_de_descuento, 'Tipos de descuento no válidos.')

    def validate_naturaleza_de_ingresos(self, naturaleza_de_ingresos):
        """Validaciones para tipo Naturaleza de ingresos

        Validaciones:
        - Relacional
        """
        return self.validacion_relacional(naturaleza_de_ingresos, 'Naturaleza de ingresos no válido.')

    def validate_fundamento_legal(self, fundamento_legal):
        """Validaciones para tipo Fundamento legal

        Validaciones:
        - Relacional
        """
        return self.validacion_relacional(fundamento_legal, 'Fundamento legal no válido.')

    def validate_fuente_de_ingreso(self, fuente_de_ingreso):
        """Validaciones para tipo Fuente de ingreso

        Validaciones:
        - Relacional
        """
        return self.validacion_relacional(fuente_de_ingreso, 'Fuente de ingreso no válido.')

    def validate_clasificador_economico(self, clasificador_economico):
        """Validaciones para tipo Clasificador economico

        Validaciones:
        - Relacional
        """
        return self.validacion_relacional(clasificador_economico, 'Clasificador económico no válido.')

    def validate_periodo_fiscal(self, periodo_fiscal):
        """Validaciones para tipo Periodo fiscal

        Validaciones:
        - Relacional
        """
        return self.validacion_relacional(periodo_fiscal, 'Período fiscal no válido.')

    def validate_padron(self, padron):
        """Validaciones Padron recargo.

        Validaciones:
        - Relacional
        """
        return self.validacion_relacional(padron, 'Padron no válido.')

    def validate_cri_clase(self, cri_clase):
        """Validaciones para Cri clase.

        Validaciones:
        - Relacional
        """
        return self.validacion_relacional(cri_clase, 'CRI clase no válida.')

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.canales_de_pago.add(self.usuario.canal_de_pago)

        return instance

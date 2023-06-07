from import_export import resources
from .models import Staff, Asset


 
class StaffResource(resources.ModelResource):

    # def before_import(self, dataset, using_transactions, dry_run, **kwargs):
    #     if not dry_run:
    #         self._meta.model.objects.delete()

    # def before_import(self, dataset, using_transactions, dry_run, **kwargs):
    #     indexes = []
    #     for i in range(0, len(dataset)):
    #         row = ''.join(dataset[i])
    #         if row.strip() == '':
    #             indexes.append(i)
    #     for index in sorted(indexes, reverse=True):
    #         del dataset[index]			
    #     return dataset        

    # def skip_row(self, instance, original):

    #     return True if Staff.objects.filter(employee_id=instance.employee_id).exists() else False
    
    class Meta:
        model = Staff
        import_id_fields = ['employee_id']
        # skip_unchanged = True
        # clean_model_instances = True

         
class AssetResource(resources.ModelResource):

    class Meta:
        model = Asset
        import_id_fields = ['asset_no']
        # skip_unchanged = True
        # clean_model_instances = True
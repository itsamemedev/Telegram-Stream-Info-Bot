# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (34)

```
  9859  GET              /                                                dashboard
 11906  GET              /api/abo/status                                  api_abo_status
 11860  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 10647  GET              /api/automation/status                           api_automation_status
 10669  POST             /api/automation/toggle                           api_automation_toggle
 19199  GET              /api/channel/categories                          api_channel_categories
 19205  POST             /api/channel/set                                 api_channel_set
 19052  GET              /api/channels/status                             api_channels_status
 18726  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 18709  GET              /api/clips                                       api_clips
 18755  POST/DELETE      /api/clips/clear                                 api_clips_clear
 18634  GET              /api/debug/threads                               api_debug_threads
 11871  GET              /api/events                                      api_events
 11355  GET              /api/events/stream                               api_events_stream
 11182  GET              /api/health                                      api_health
 18668  POST             /api/highlights/config                           api_highlights_config
  9793  POST             /api/login                                       dashboard_login_submit
 12196  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 11270  GET              /api/notify/status                               api_notify_status
 11281  POST             /api/notify/test                                 api_notify_test
 11960  GET              /api/proxy/heatmap                               api_proxy_heatmap
 11937  GET              /api/proxy/trend                                 api_proxy_trend
 18775  GET              /api/tts/<fn>                                    api_tts_file
 19550  GET              /api/upload_window                               api_upload_window
 11472  GET              /archive/<int:eid>/download                      archive_download
 11500  GET              /download/<int:recording_id>                     download
 11429  GET              /health                                          health
 18580  GET              /healthz                                         healthz
  9784  GET              /login                                           dashboard_login_page
  9814  GET              /logout                                          dashboard_logout
  9821  GET              /manifest.webmanifest                            pwa_manifest
 19523  GET              /overlay                                         overlay_page
  9845  GET              /pwa-icon-<variant>.png                          pwa_icon
  9831  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (335)

```
   183  GET              /api/active-recordings                           api_active_recordings   [nc/routes/auskunft.py]
   410  GET              /api/activity-pulse                              api_activity_pulse   [nc/routes/auskunft.py]
   195  GET              /api/ai-log                                      api_ai_log   [nc/routes/stats.py]
   165  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail   [nc/routes/stats.py]
   993  GET              /api/ai/anomalies                                api_ai_anomalies   [nc/routes/ai.py]
   738  POST             /api/ai/ask                                      api_ai_ask   [nc/routes/ai.py]
   864  POST             /api/ai/claude/save                              api_claude_save   [nc/routes/ai.py]
   844  GET              /api/ai/claude/status                            api_claude_status   [nc/routes/ai.py]
   882  POST             /api/ai/claude/test                              api_claude_test   [nc/routes/ai.py]
   806  GET              /api/ai/config                                   api_ai_config   [nc/routes/ai.py]
   356  GET              /api/ai/conversations                            api_ai_conversations_list   [nc/routes/ai.py]
   367  POST             /api/ai/conversations                            api_ai_conversations_create   [nc/routes/ai.py]
   377  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get   [nc/routes/ai.py]
   400  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete   [nc/routes/ai.py]
   407  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch   [nc/routes/ai.py]
   418  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send   [nc/routes/ai.py]
   546  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream   [nc/routes/ai.py]
   644  POST             /api/ai/diagnose                                 api_ai_diagnose   [nc/routes/ai.py]
  1231  GET              /api/ai/forecast-storage                         api_ai_forecast_storage   [nc/routes/ai.py]
  1263  GET              /api/ai/health-score/<username>                  api_ai_health_score   [nc/routes/ai.py]
   341  GET              /api/ai/models                                   api_ai_models   [nc/routes/ai.py]
   946  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive   [nc/routes/ai.py]
   926  POST             /api/ai/query                                    api_ai_query   [nc/routes/ai.py]
  1099  GET              /api/ai/recommendations                          api_ai_recommendations   [nc/routes/ai.py]
  1147  GET              /api/ai/report                                   api_ai_report   [nc/routes/ai.py]
  1198  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice   [nc/routes/ai.py]
  1057  GET              /api/ai/segments                                 api_ai_segments   [nc/routes/ai.py]
   901  GET              /api/ai/skills                                   api_ai_skills   [nc/routes/ai.py]
   499  GET              /api/archive                                     api_archive   [nc/routes/archive.py]
   763  DELETE           /api/archive/<int:eid>                           api_archive_delete   [nc/routes/archive.py]
   645  POST             /api/archive/<int:eid>/rename                    api_archive_rename   [nc/routes/archive.py]
   628  POST             /api/archive/bulk-delete                         api_archive_bulk_delete   [nc/routes/archive.py]
   620  GET              /api/archive/check                               api_archive_check   [nc/routes/archive.py]
   456  GET              /api/archive/duplicates                          api_archive_duplicates   [nc/routes/archive.py]
   472  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete   [nc/routes/archive.py]
   807  POST             /api/archive/index/<int:rid>                     api_archive_index_one   [nc/routes/archive.py]
   374  GET              /api/archive/scan                                api_archive_scan   [nc/routes/archive.py]
   405  POST             /api/archive/scan/adopt                          api_archive_scan_adopt   [nc/routes/archive.py]
   772  GET              /api/archive/search                              api_archive_search   [nc/routes/archive.py]
   792  GET              /api/archive/status                              api_archive_status   [nc/routes/archive.py]
   679  POST             /api/archive/upload                              api_archive_upload   [nc/routes/archive.py]
    49  GET/POST         /api/audio/config                                api_audio_config   [nc/routes/audio.py]
    78  POST             /api/audio/testtone                              api_audio_testtone   [nc/routes/audio.py]
   216  GET/POST         /api/auto-archive-rules                          api_archive_rules   [nc/routes/wartung.py]
   241  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete   [nc/routes/wartung.py]
   246  POST             /api/auto-archive-rules/run                      api_archive_rules_run   [nc/routes/wartung.py]
   163  GET              /api/azrael/agents                               api_azrael_agents   [nc/routes/azrael.py]
    99  POST             /api/azrael/ask                                  api_azrael_ask   [nc/routes/azrael.py]
   222  GET/POST         /api/azrael/context                              api_azrael_context   [nc/routes/azrael.py]
   120  GET              /api/azrael/core                                 api_azrael_core   [nc/routes/azrael.py]
   342  POST             /api/azrael/live_pause                           api_azrael_live_pause   [nc/routes/azrael.py]
   328  GET              /api/azrael/live_status                          api_azrael_live_status   [nc/routes/azrael.py]
   350  POST             /api/azrael/live_test                            api_azrael_live_test   [nc/routes/azrael.py]
   174  GET              /api/azrael/memories                             api_azrael_memories   [nc/routes/azrael.py]
   406  POST             /api/azrael/persona                              api_azrael_persona_set   [nc/routes/azrael.py]
   397  GET              /api/azrael/personas                             api_azrael_personas   [nc/routes/azrael.py]
   314  GET              /api/azrael/piper_status                         api_azrael_piper_status   [nc/routes/azrael.py]
   190  POST             /api/azrael/react                                api_azrael_react   [nc/routes/azrael.py]
   231  GET              /api/azrael/reaction                             api_azrael_reaction   [nc/routes/azrael.py]
   243  GET              /api/azrael/reactions                            api_azrael_reactions   [nc/routes/azrael.py]
   372  GET              /api/azrael/transcript                           api_azrael_transcript   [nc/routes/azrael.py]
   281  POST             /api/azrael/tts_test                             api_azrael_tts_test   [nc/routes/azrael.py]
   267  GET              /api/azrael/voices                               api_azrael_voices   [nc/routes/azrael.py]
   379  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model   [nc/routes/azrael.py]
   286  GET              /api/backoff-watch                               api_backoff_watch   [nc/routes/beobachtung.py]
   208  POST             /api/backup/run                                  api_backup_run   [nc/routes/wartung.py]
   174  GET              /api/backup/status                               api_backup_status   [nc/routes/wartung.py]
   157  POST             /api/backup/system                               api_backup_system   [nc/routes/wartung.py]
   387  GET              /api/bandwidth/live                              api_bandwidth_live   [nc/routes/auskunft.py]
   364  GET              /api/bookmarks                                   api_bookmarks_list   [nc/routes/auskunft.py]
   198  GET              /api/brain                                       api_brain   [nc/routes/brain.py]
   131  GET              /api/brain/alarms                                api_brain_alarms   [nc/routes/brain.py]
   116  GET              /api/brain/creator                               api_brain_creator   [nc/routes/brain.py]
    93  GET              /api/brain/graph                                 api_brain_graph   [nc/routes/brain.py]
   158  GET              /api/brain/growth                                api_brain_growth   [nc/routes/brain.py]
    80  GET              /api/brain/health                                api_brain_health   [nc/routes/brain.py]
    81  POST             /api/chat/send                                   api_chat_send   [nc/routes/chat.py]
    53  GET              /api/chat/send_status                            api_chat_send_status   [nc/routes/chat.py]
   162  GET              /api/checks                                      api_checks   [nc/routes/auskunft.py]
    40  GET              /api/cohost                                      api_cohost   [nc/routes/cohost.py]
    52  POST             /api/cohost/config                               api_cohost_config   [nc/routes/cohost.py]
    52  GET/POST         /api/collections                                 api_collections   [nc/routes/collections.py]
    87  POST/DELETE      /api/collections/<int:cid>                       api_collection_modify   [nc/routes/collections.py]
   122  GET              /api/collections/<int:cid>/trackings             api_collection_trackings   [nc/routes/collections.py]
   431  GET              /api/community/stats                             api_community_stats   [nc/routes/auskunft.py]
   433  POST             /api/config/restore                              api_config_restore   [nc/routes/settings.py]
   418  GET              /api/config/snapshot                             api_config_snapshot   [nc/routes/settings.py]
   238  GET              /api/cookies/age                                 api_cookies_age   [nc/routes/settings.py]
   195  POST             /api/cookies/fetch                               api_cookies_fetch   [nc/routes/settings.py]
    73  GET              /api/cookies/health                              api_cookies_health   [nc/routes/settings.py]
    80  POST             /api/cookies/update                              api_cookies_update   [nc/routes/settings.py]
   485  GET              /api/data/export                                 api_data_export   [nc/routes/auskunft.py]
   259  GET              /api/db/export                                   api_db_export   [nc/routes/settings.py]
   286  POST             /api/db/import                                   api_db_import   [nc/routes/settings.py]
   379  POST             /api/db/restore/apply                            api_db_restore_apply   [nc/routes/settings.py]
   323  GET              /api/db/restore/list                             api_db_restore_list   [nc/routes/settings.py]
   341  POST             /api/db/restore/prepare                          api_db_restore_prepare   [nc/routes/settings.py]
   246  GET              /api/db/summary                                  api_db_summary   [nc/routes/settings.py]
   164  GET              /api/defense/attacks                             api_defense_attacks   [nc/routes/abwehr.py]
   125  GET              /api/defense/crowdsec                            api_defense_crowdsec   [nc/routes/abwehr.py]
   146  GET              /api/defense/fail2ban                            api_defense_fail2ban   [nc/routes/abwehr.py]
    91  GET              /api/defense/overview                            api_defense_overview   [nc/routes/abwehr.py]
   244  POST             /api/discord/announce                            api_discord_announce   [nc/routes/discord.py]
   170  GET              /api/discord/clips_week                          api_discord_clips_week   [nc/routes/discord.py]
   188  GET              /api/discord/community                           api_discord_community   [nc/routes/discord.py]
   160  GET              /api/discord/invite                              api_discord_invite   [nc/routes/discord.py]
    63  GET              /api/discord/overview                            api_discord_overview   [nc/routes/discord.py]
   136  POST             /api/discord/webhook_test                        api_discord_webhook_test   [nc/routes/discord.py]
    79  POST             /api/donations/add                               api_donations_add   [nc/routes/money.py]
   112  GET              /api/donations/manual                            api_donations_manual   [nc/routes/money.py]
   120  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete   [nc/routes/money.py]
    60  POST             /api/donations/reset                             api_donations_reset   [nc/routes/money.py]
   136  GET              /api/donations/summary                           api_donations_summary   [nc/routes/money.py]
   194  GET              /api/evolution/changelog                         api_evolution_changelog   [nc/routes/evolution.py]
   179  GET              /api/evolution/history                           api_evolution_history   [nc/routes/evolution.py]
    90  GET              /api/evolution/learned                           api_evolution_learned   [nc/routes/evolution.py]
   112  GET              /api/evolution/proposals                         api_evolution_proposals   [nc/routes/evolution.py]
   133  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss   [nc/routes/evolution.py]
   150  POST             /api/evolution/proposals/bulk                    api_evolution_bulk   [nc/routes/evolution.py]
    80  POST             /api/evolution/run                               api_evolution_run   [nc/routes/evolution.py]
   209  GET              /api/evolution/snapshots                         api_evolution_snapshots   [nc/routes/evolution.py]
    44  GET              /api/evolution/status                            api_evolution_status   [nc/routes/evolution.py]
   200  GET              /api/finanzamt/entries                           api_finanzamt_entries   [nc/routes/money.py]
   220  POST             /api/finanzamt/entry                             api_finanzamt_add   [nc/routes/money.py]
   247  GET              /api/finanzamt/export.csv                        api_finanzamt_csv   [nc/routes/money.py]
   382  GET              /api/forecast/storage                            api_forecast_storage   [nc/routes/auskunft.py]
   285  GET              /api/freeai/status                               api_freeai_status   [nc/routes/auskunft.py]
    36  GET              /api/health-score                                api_health_score   [nc/routes/health.py]
   402  GET              /api/heatmap/lives/<username>                    api_heatmap_lives   [nc/routes/auskunft.py]
   397  GET              /api/heatmap/recordings                          api_heatmap_recordings   [nc/routes/auskunft.py]
   473  GET              /api/highlights                                  api_highlights   [nc/routes/auskunft.py]
    64  GET              /api/i18n/katalog                                api_i18n_katalog   [nc/routes/i18n.py]
    53  GET              /api/i18n/sprachen                               api_i18n_sprachen   [nc/routes/i18n.py]
   307  GET              /api/i18n/uebersetzer.js                         api_i18n_js   [nc/routes/i18n.py]
    77  POST             /api/i18n/waehlen                                api_i18n_waehlen   [nc/routes/i18n.py]
   168  GET              /api/insights/activity-clock                     api_insights_activity_clock   [nc/routes/insights.py]
    43  GET              /api/insights/best-times/<username>              api_insights_best_times   [nc/routes/insights.py]
   150  GET              /api/insights/catch-rate                         api_insights_catch_rate   [nc/routes/insights.py]
   125  GET              /api/insights/growth/<username>                  api_insights_growth   [nc/routes/insights.py]
   189  GET              /api/insights/leaderboard                        api_insights_leaderboard   [nc/routes/insights.py]
    76  GET              /api/insights/reliability                        api_insights_reliability   [nc/routes/insights.py]
    99  GET              /api/insights/session-stats                      api_insights_session_stats   [nc/routes/insights.py]
   223  GET              /api/insights/storage-by-streamer                api_insights_storage_by_streamer   [nc/routes/insights.py]
   222  GET              /api/kick/channel                                api_kick_channel   [nc/routes/kick.py]
   244  POST             /api/kick/channel                                api_kick_channel_set   [nc/routes/kick.py]
   103  GET              /api/kick/oauth/callback                         api_kick_oauth_callback   [nc/routes/kick.py]
   171  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect   [nc/routes/kick.py]
   149  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect   [nc/routes/kick.py]
    85  GET              /api/kick/oauth/start                            api_kick_oauth_start   [nc/routes/kick.py]
   128  GET              /api/kick/oauth/status                           api_kick_oauth_status   [nc/routes/kick.py]
   178  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck   [nc/routes/kick.py]
   119  POST             /api/kickmod/config                              api_kickmod_config   [nc/routes/kickmod.py]
   167  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords   [nc/routes/kickmod.py]
   184  GET              /api/kickmod/learned                             api_kickmod_learned   [nc/routes/kickmod.py]
   215  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear   [nc/routes/kickmod.py]
   191  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote   [nc/routes/kickmod.py]
   251  POST             /api/kickmod/say                                 api_kickmod_say   [nc/routes/kickmod.py]
   221  POST             /api/kickmod/start                               api_kickmod_start   [nc/routes/kickmod.py]
    82  GET              /api/kickmod/status                              api_kickmod_status   [nc/routes/kickmod.py]
   235  POST             /api/kickmod/stop                                api_kickmod_stop   [nc/routes/kickmod.py]
   416  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard   [nc/routes/auskunft.py]
    78  POST             /api/marketing/config                            api_marketing_config   [nc/routes/marketing.py]
   103  GET              /api/marketing/preview                           api_marketing_preview   [nc/routes/marketing.py]
   113  POST             /api/marketing/send-now                          api_marketing_send_now   [nc/routes/marketing.py]
    52  GET              /api/marketing/status                            api_marketing_status   [nc/routes/marketing.py]
    70  POST             /api/marketing/toggle                            api_marketing_toggle   [nc/routes/marketing.py]
   225  GET              /api/moderation/feed                             api_moderation_feed   [nc/routes/stats.py]
   100  POST             /api/news/config                                 api_news_config   [nc/routes/news.py]
    66  GET              /api/news/creators                               api_news_creators   [nc/routes/news.py]
    77  POST             /api/news/creators/generate                      api_news_creators_generate   [nc/routes/news.py]
   142  POST             /api/news/generate-now                           api_news_generate_now   [nc/routes/news.py]
   137  GET              /api/news/items                                  api_news_items   [nc/routes/news.py]
   128  GET              /api/news/preview                                api_news_preview   [nc/routes/news.py]
    53  GET              /api/news/status                                 api_news_status   [nc/routes/news.py]
    92  POST             /api/news/toggle                                 api_news_toggle   [nc/routes/news.py]
   257  GET              /api/ops/audit                                   api_ops_audit   [nc/routes/ops.py]
   324  GET              /api/ops/db-stats                                api_ops_db_stats   [nc/routes/ops.py]
   352  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown   [nc/routes/ops.py]
   203  GET              /api/ops/errors                                  api_ops_errors   [nc/routes/ops.py]
   270  GET              /api/ops/healthcheck                             api_ops_healthcheck   [nc/routes/ops.py]
   505  GET              /api/ops/log-tail                                api_ops_log_tail   [nc/routes/ops.py]
    80  GET              /api/ops/logtail                                 api_ops_logtail   [nc/routes/ops.py]
   168  GET              /api/ops/metrics                                 api_ops_metrics   [nc/routes/ops.py]
   151  GET              /api/ops/resource_history                        api_ops_resource_history   [nc/routes/ops.py]
   391  GET              /api/ops/version                                 api_ops_version   [nc/routes/ops.py]
   226  GET              /api/outcomes                                    api_outcomes   [nc/routes/auskunft.py]
   210  POST             /api/overlay/config                              api_overlay_config   [nc/routes/overlay.py]
   193  POST             /api/overlay/event                               api_overlay_event   [nc/routes/overlay.py]
    94  GET              /api/overlay/state                               api_overlay_state   [nc/routes/overlay.py]
   177  GET              /api/profile/<username>                          api_profile   [nc/routes/beobachtung.py]
   460  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk   [nc/routes/beobachtung.py]
   435  GET              /api/profile/snapshots/<username>                api_profile_snapshots   [nc/routes/beobachtung.py]
   296  GET              /api/public/stats                                api_public_stats   [nc/routes/auskunft.py]
   143  GET              /api/pulse                                       api_pulse   [nc/routes/auskunft.py]
   944  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
  1053  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
  1081  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
  1101  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   931  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
   993  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
   980  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
   961  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
   335  GET              /api/recording-attempts                          api_recording_attempts   [nc/routes/auskunft.py]
   606  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations   [nc/routes/recordings.py]
   601  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark   [nc/routes/recordings.py]
   649  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint   [nc/routes/recordings.py]
   532  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect   [nc/routes/recordings.py]
   859  POST             /api/recordings/<int:rid>/label                  api_recording_label   [nc/routes/recordings.py]
   623  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest   [nc/routes/recordings.py]
   586  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes   [nc/routes/recordings.py]
   559  GET              /api/recordings/<int:rid>/quality                api_recording_quality   [nc/routes/recordings.py]
   833  POST             /api/recordings/<int:rid>/rating                 api_recording_rating   [nc/routes/recordings.py]
   703  POST             /api/recordings/<int:rid>/restore                api_recording_restore   [nc/routes/recordings.py]
   792  POST             /api/recordings/<int:rid>/star                   api_recording_star   [nc/routes/recordings.py]
   698  POST             /api/recordings/<int:rid>/trash                  api_recording_trash   [nc/routes/recordings.py]
   631  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform   [nc/routes/recordings.py]
   411  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop   [nc/routes/recordings.py]
   876  GET              /api/recordings/by-label/<label>                 api_recordings_by_label   [nc/routes/recordings.py]
   499  GET              /api/recordings/daily                            api_recordings_daily   [nc/routes/recordings.py]
   754  POST             /api/recordings/dedup-scan                       api_dedup_scan   [nc/routes/recordings.py]
   909  GET              /api/recordings/disconnects                      api_recording_disconnects   [nc/routes/recordings.py]
   894  GET              /api/recordings/labels                           api_recordings_labels   [nc/routes/recordings.py]
   455  GET              /api/recordings/list                             api_recordings_list   [nc/routes/recordings.py]
   693  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop   [nc/routes/recordings.py]
   679  GET              /api/recordings/manual/list                      api_manual_list   [nc/routes/recordings.py]
   662  POST             /api/recordings/manual/start                     api_manual_start   [nc/routes/recordings.py]
   719  GET              /api/recordings/overview                         api_recordings_overview   [nc/routes/recordings.py]
  1244  GET              /api/recordings/session/<sid>                    api_recording_session   [nc/routes/recordings.py]
  1319  POST             /api/recordings/session/<sid>/join               api_recording_session_join   [nc/routes/recordings.py]
  1208  GET              /api/recordings/sessions                         api_recording_sessions   [nc/routes/recordings.py]
   812  GET              /api/recordings/starred                          api_recordings_starred   [nc/routes/recordings.py]
   708  GET              /api/recordings/trash                            api_trash_list   [nc/routes/recordings.py]
   486  POST             /api/restream/<int:rid>/delete                   api_restream_delete   [nc/routes/restream.py]
   464  POST             /api/restream/<int:rid>/edit                     api_restream_edit   [nc/routes/restream.py]
   505  POST             /api/restream/<int:rid>/start                    api_restream_start   [nc/routes/restream.py]
   522  POST             /api/restream/<int:rid>/stop                     api_restream_stop   [nc/routes/restream.py]
   574  GET              /api/restream/chatfeed                           api_restream_chatfeed   [nc/routes/restream.py]
   440  POST             /api/restream/create                             api_restream_create   [nc/routes/restream.py]
   265  GET              /api/restream/deck                               api_restream_deck   [nc/routes/restream.py]
   165  GET              /api/restream/health                             api_restream_health   [nc/routes/restream.py]
   596  POST             /api/restream/layout                             api_restream_layout   [nc/routes/restream.py]
   413  GET              /api/restream/list                               api_restream_list   [nc/routes/restream.py]
   134  POST             /api/restream/report                             api_restream_report   [nc/routes/restream.py]
   535  POST             /api/restream/start_all                          api_restream_start_all   [nc/routes/restream.py]
   561  POST             /api/restream/stop_all                           api_restream_stop_all   [nc/routes/restream.py]
   191  GET              /api/restream/testpush                           api_testpush_status   [nc/routes/restream.py]
   216  POST             /api/restream/testpush                           api_testpush_run   [nc/routes/restream.py]
   388  GET              /api/restream/verify                             api_restream_verify   [nc/routes/restream.py]
   134  GET              /api/retention/preview                           api_retention_preview   [nc/routes/wartung.py]
   144  POST             /api/retention/run                               api_retention_run   [nc/routes/wartung.py]
   474  POST             /api/schedule/add                                api_schedule_add   [nc/routes/settings.py]
   464  GET              /api/schedule/list                               api_schedule_list   [nc/routes/settings.py]
   499  POST             /api/schedule/remove                             api_schedule_remove   [nc/routes/settings.py]
    65  POST             /api/scheduler/add                               api_scheduler_add   [nc/routes/scheduler.py]
    86  POST             /api/scheduler/delete                            api_scheduler_delete   [nc/routes/scheduler.py]
    52  GET              /api/scheduler/list                              api_scheduler_list   [nc/routes/scheduler.py]
   102  POST             /api/scheduler/toggle                            api_scheduler_toggle   [nc/routes/scheduler.py]
   354  GET              /api/search                                      api_search   [nc/routes/auskunft.py]
    92  GET              /api/selftest                                    api_selftest   [nc/routes/selbsttest.py]
   444  GET              /api/shield/stats                                api_shield_stats   [nc/routes/auskunft.py]
   128  GET              /api/stats                                       api_stats   [nc/routes/stats.py]
   219  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern   [nc/routes/stats.py]
   214  GET              /api/stats/tiktok-status                         api_tiktok_status   [nc/routes/stats.py]
   274  GET              /api/stats/timeline                              api_stats_timeline   [nc/routes/stats.py]
   110  GET              /api/storage                                     api_storage   [nc/routes/wartung.py]
   116  POST             /api/storage/cleanup                             api_storage_cleanup   [nc/routes/wartung.py]
   448  GET              /api/stream/inspect/<username>                   api_stream_inspect   [nc/routes/beobachtung.py]
   340  GET              /api/stream/timeline                             api_stream_timeline   [nc/routes/beobachtung.py]
   370  GET              /api/stream/transcript                           api_stream_transcript   [nc/routes/beobachtung.py]
   126  GET              /api/streamer/compare                            api_streamer_compare   [nc/routes/streamer.py]
   273  POST             /api/streamer/delete/<username>                  api_streamer_delete   [nc/routes/streamer.py]
    88  GET              /api/streamer/detail                             api_streamer_detail   [nc/routes/streamer.py]
   298  GET              /api/streamer/digest/<username>                  api_streamer_digest   [nc/routes/streamer.py]
   230  GET              /api/streamer/dormant                            api_streamer_dormant   [nc/routes/streamer.py]
   254  GET              /api/streamer/exists/<username>                  api_streamer_exists   [nc/routes/streamer.py]
   185  GET              /api/streamer/journal/<username>                 api_streamer_journal   [nc/routes/streamer.py]
   150  GET/POST         /api/streamer/priority/<username>                api_streamer_priority   [nc/routes/streamer.py]
   210  GET              /api/streamer/watchlist                          api_streamer_watchlist   [nc/routes/streamer.py]
    56  GET              /api/streamers/wall                              api_streamers_wall   [nc/routes/streamer.py]
   207  GET              /api/summary/preview                             api_summary_preview   [nc/routes/auskunft.py]
    73  GET              /api/system                                      api_system   [nc/routes/systemlage.py]
   116  GET              /api/system-resources                            api_system_resources   [nc/routes/health.py]
   177  GET              /api/system/check_timing                         api_check_timing   [nc/routes/systemlage.py]
   117  GET              /api/system/config_drift                         api_config_drift   [nc/routes/systemlage.py]
   140  GET              /api/system/config_snapshot                      api_system_config_snapshot   [nc/routes/systemlage.py]
   237  GET              /api/system/preflight                            api_system_preflight   [nc/routes/systemlage.py]
   104  GET              /api/system/preflight_history                    api_system_preflight_history   [nc/routes/systemlage.py]
   369  GET              /api/system/resilience                           api_system_resilience   [nc/routes/systemlage.py]
   377  GET              /api/tags                                        api_tags_list   [nc/routes/auskunft.py]
   177  GET              /api/top                                         api_top   [nc/routes/auskunft.py]
   238  GET              /api/trackings                                   api_trackings   [nc/routes/trackings.py]
   453  POST             /api/trackings/<int:tid>/collection              api_tracking_collection   [nc/routes/trackings.py]
   482  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration   [nc/routes/trackings.py]
   402  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority   [nc/routes/trackings.py]
   415  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart   [nc/routes/trackings.py]
   511  GET              /api/trackings/<int:tid>/settings                api_tracking_settings   [nc/routes/trackings.py]
   388  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags   [nc/routes/trackings.py]
   263  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes   [nc/routes/trackings.py]
   308  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause   [nc/routes/trackings.py]
   332  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck   [nc/routes/trackings.py]
   319  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume   [nc/routes/trackings.py]
   165  POST             /api/trackings/bulk                              api_trackings_bulk   [nc/routes/trackings.py]
   277  GET              /api/trackings/export                            api_trackings_export   [nc/routes/trackings.py]
   135  GET              /api/trackings/groups                            api_trackings_groups   [nc/routes/trackings.py]
   369  GET              /api/trackings/tags-map                          api_trackings_tags_map   [nc/routes/trackings.py]
   424  GET              /api/trackings/watchlist-export                  api_watchlist_export   [nc/routes/trackings.py]
   253  GET              /api/trend-7d                                    api_trend_7d   [nc/routes/auskunft.py]
   121  POST             /api/tunnel/set                                  api_tunnel_set   [nc/routes/ops.py]
   100  GET              /api/tunnel/status                               api_tunnel_status   [nc/routes/ops.py]
   132  POST             /api/tunnel/test                                 api_tunnel_test   [nc/routes/ops.py]
   113  POST             /api/tunnel/toggle                               api_tunnel_toggle   [nc/routes/ops.py]
   125  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback   [nc/routes/twitch.py]
    77  POST             /api/twitch/oauth/redirect                       api_twitch_oauth_redirect   [nc/routes/twitch.py]
   101  GET              /api/twitch/oauth/start                          api_twitch_oauth_start   [nc/routes/twitch.py]
    55  GET              /api/twitch/oauth/status                         api_twitch_oauth_status   [nc/routes/twitch.py]
   453  GET              /api/update/backups                              api_update_backups   [nc/routes/ops.py]
   419  GET              /api/update/check                                api_update_check   [nc/routes/ops.py]
   478  POST             /api/update/restart                              api_update_restart   [nc/routes/ops.py]
   458  POST             /api/update/rollback                             api_update_rollback   [nc/routes/ops.py]
   441  POST             /api/update/start                                api_update_start   [nc/routes/ops.py]
   434  GET              /api/update/status                               api_update_status   [nc/routes/ops.py]
   239  GET              /api/userstats                                   api_userstats   [nc/routes/auskunft.py]
   305  GET              /api/version                                     api_version   [nc/routes/auskunft.py]
    52  GET/POST         /api/webhooks                                    api_webhooks   [nc/routes/webhooks.py]
    92  DELETE           /api/webhooks/<int:wid>                          api_webhook_delete   [nc/routes/webhooks.py]
   123  POST             /api/webhooks/<int:wid>/test                     api_webhook_test   [nc/routes/webhooks.py]
   107  POST             /api/webhooks/<int:wid>/toggle                   api_webhook_toggle   [nc/routes/webhooks.py]
   131  GET              /api/youtube/oauth/callback                      api_youtube_oauth_callback   [nc/routes/youtube.py]
   152  POST             /api/youtube/oauth/forget                        api_youtube_oauth_forget   [nc/routes/youtube.py]
   164  POST             /api/youtube/oauth/logout                        api_youtube_oauth_logout   [nc/routes/youtube.py]
    89  POST             /api/youtube/oauth/redirect                      api_youtube_oauth_redirect   [nc/routes/youtube.py]
   113  GET              /api/youtube/oauth/start                         api_youtube_oauth_start   [nc/routes/youtube.py]
    67  GET              /api/youtube/oauth/status                        api_youtube_oauth_status   [nc/routes/youtube.py]
   199  GET              /api/youtube/sendrate                            api_youtube_sendrate   [nc/routes/youtube.py]
   382  GET              /metrics                                         api_prometheus_metrics   [nc/routes/beobachtung.py]
```

## Discord-Slash-Commands in discordbot.py (65)

```
  2080  /about                  Ueber diesen Bot
   809  /ai                     
  2080  /aireset                KI-Kontext zuruecksetzen
  1213  /ask                    
   910  /assign_role            
   960  /ban                    
  2035  /botstats               
  2080  /brain                  Brain-Lage: Regeln, Agenten, Empfehlungen
  2080  /bulkadd                Mehrere User auf einmal tracken · a b c
  2080  /cleanup                Alte Aufnahmen aufraeumen
  1468  /clearwarns             
  1999  /clip                   
  1984  /clipoftheweek          
  1339  /clips                  
  2080  /cookies                Cookie-Status — mit 'holen' selbst beziehen · [holen]
   865  /create_category        
   836  /create_channel         
   900  /create_group           
   875  /create_role            
   851  /create_voice           
  1096  /daily                  
  2080  /diag                   Vollstaendige Diagnose
  2080  /einnahmen              Einnahmen und Spenden
  1242  /event                  
  1284  /events                 
  1378  /follow                 
  1367  /help                   
   950  /kick                   
  1071  /leaderboard            
  2080  /live                   Live-Status sofort pruefen · @user
  1326  /livenow                
  2080  /logs                   Letzte Fehler aus dem Log
  2080  /pause                  Tracking pausieren · @user
  1354  /post_test              
  1174  /profile                
   982  /purge                  
  2080  /quota                  Speicher-Quota
  1058  /rank                   
  1314  /recstatus              
   920  /remove_role            
  2080  /report                 Azrael-Sentinel-Wochenreport
   822  /restream_status        
  2080  /resume                 Tracking fortsetzen · @user
   930  /set_channel_perms      
  1025  /setup_community        
  1042  /setup_targets          
  1410  /stats                  
   781  /status                 
  2080  /stoprec                Laufende Aufnahme sauber beenden · @user
  1506  /streaminfo             
  2080  /summary                Tageszusammenfassung
  2080  /sysres                 System-Ressourcen
  2080  /teststream             Recorder-Selbsttest · @user
  2080  /tiktok                 Profil-Analyse eines TikTok-Accounts · ‹name›
   970  /timeout                
  1478  /topstreamers           
  2080  /topusers               Top-Streamer nach Aufnahmen
   711  /track                  
  2080  /track_exact            Exakten Usernamen tracken (ohne Korrektur) · ‹name›
   794  /tracklist              
  1392  /unfollow               
  2080  /unpause                Auto-pausierte Quelle wieder aktivieren · @user
   743  /untrack                
  1431  /warn                   
  1454  /warnings               
```

## Discord-Events in discordbot.py (4)

```
  2238  on_member_join
  2200  on_message
  2101  on_raw_reaction_add
  2273  on_ready
```

## Top-Level-Symbole in telegramversand.py (2 Funktionen)

```
    58-73     konfiguriere
    76-456    split_and_send_video
```

## Top-Level-Symbole in discordbot.py (46 Funktionen)

```
  1583-1634   _award_xp
  1803-1832   _clip_week_leader
  1856-1870   _clipoftheweek_loop
  2389-2451   _community_events_loop
  1540-1562   _dc_client
  1565-1574   _dc_offen
  2491-2526   _disc_automod_check
   401-406    _disc_sprache_setzen
  1637-1685   _discord_ai_automod
   534-573    _discord_automod
  1688-1708   _discord_azrael_reply
  1873-2348   _discord_run_once
   236-294    _discord_start
   297-351    _ensure_discord_invite
  2354-2386   _ensure_error_channel
   422-435    _ensure_rank_roles
   674-688    _ensure_team_roles
  2454-2484   _error_channel_loop
   583-587    _guard
   503-531    _handle_voice_ai
   409-419    _is_admin
  1751-1762   _liveboard_loop
   590-608    _on_level_up
   499-500    _par_chat_id
  1835-1853   _post_clip_of_week
  1765-1783   _post_weekly_digest
   438-464    _provision_base_channels
   467-483    _provision_user_channels
  1306-1399   _reg_betrieb
   996-1085   _reg_community_setup
  1088-1163   _reg_daily_profil
  1206-1303   _reg_frage_events
   768-824    _reg_info
   942-993    _reg_moderation
  1166-1203   _reg_profil
   891-939    _reg_rollen
   827-888    _reg_server
  1402-1489   _reg_streamer
  1492-1537   _reg_system
   702-765    _reg_tracking
   643-671    _run_tg_handler
   486-496    _tracked_usernames
   153-215    _uebernehmen
  1717-1748   _update_liveboard
  1786-1800   _weekly_digest_loop
   218-221    starte
```

## Top-Level-Symbole in bot.py (517 Funktionen, 2 Klassen)

```
 24089-24111  _abbruch_datenbank_unlesbar
  2621-2622   _abo_key
  2642-2660   _abo_probe_dump
 24162-24180  _abschluss
 15505-15512  _ad_allowlist
 16485-16491  _agent_for
 16494-16510  _ai_telemetry
 17005-17023  _alert
 20410-20460  _alert_monitor_loop
 20812-20874  _announce_loop
  3474-3484   _anthropic_key
  3491-3493   _anthropic_model
  9479-9482   _arg_int
  2613-2618   _as_dict
 23839-23848  _async_exc_handler
 17186-17208  _audio_tap_cmd
 17766-17825  _audio_tap_melden
 17222-17246  _audio_tap_sammler
 24114-24149  _aufraeumen
  9647-9716   _auth_cookie
  9614-9643   _auth_guard
  1872-1877   _auto_on
 18442-18460  _auto_restream_loop
 13376-13418  _avatar_frames_laden
 21892-21907  _azrael_broadcast_reply
 21792-21814  _azrael_chat_reply
 21764-21789  _azrael_chat_should_reply
 21820-21822  _azrael_gate_cfg
 16515-16529  _azrael_live_state
 19436-19450  _azrael_overlay_state
 16887-16941  _azrael_proactive_loop
 16333-16389  _azrael_reaction_to_chats
 21825-21832  _azrael_reply_all_chats
 21751-21761  _azrael_self_names
 21860-21889  _azrael_send_to
 13337-13373  _azrael_spricht
 16535-16556  _azrael_system
 20544-20547  _backup_active
 20625-20638  _backup_loop
 23912-23921  _brain_crowdsec_snap
 20331-20340  _brain_growth_loop
 10038-10065  _brain_growth_snapshot
  2555-2575   _brain_hint_delay
 23984-24019  _brain_moderation_snap
  6370-6398   _brain_notify
 24022-24044  _brain_recording_snap
 23924-23981  _brain_restream_health
 24047-24060  _brain_tiktok_status_snap
 11334-11351  _browser_push
  6410-6497   _build_daily_summary
 13697-13701  _build_restream_cmd
  5192-5219   _can_stop_tracking
  1985-2007   _capture_set_cookies
 12014-12017  _cfg_get
 12020-12022  _cfg_set
 19160-19195  _channel_set_all
 12565-12568  _chat_connected
 12571-12587  _chat_disconnected
  8536-8547   _chat_is_forum
 17573-17598  _chat_listener_abbauen
 12607-12609  _chat_sanitize
 12550-12562  _chat_stat
 12590-12593  _chat_stats_snapshot
  3786-3798   _check_ai_models_sync
 10320-10363  _classify_pool_anonymity
 10366-10383  _classify_pool_anonymity_bg
   868-890    _claude_chat_sync_metered
  9508-9515   _client_ip
 20958-20985  _clip_prune
 20988-20998  _clip_recfile_for
 21408-21414  _clip_should_velocity
 21039-21121  _clip_to_discord
  3672-3681   _close_ai_session
 21938-21953  _cohost_broadcast
 21923-21924  _cohost_cfg
 21979-21991  _cohost_fire_highlight
 21927-21935  _cohost_gate
 21956-21976  _cohost_highlight
  9968-9970   _conv_messages
  6769-6830   _cookie_alarm_loop
  2075-2076   _cookie_autofetch_info
  2059-2063   _cookie_autorefresh_info
 23549-23571  _cookie_bezug_loop
 23574-23599  _cookie_bezug_runde
  1962-1966   _cookie_header
  2088-2102   _cookies_selbst_holen
  4022-4034   _create_index_safe
 19882-19988  _crowdsec_status
 19828-19879  _crowdsec_via_lapi
 19732-19750  _cscli_bin
 19759-19772  _cscli_path
  6659-6684   _daily_summary_loop
 19790-19807  _darf_journal_lesen
  3038-3063   _darf_ytdlp_nachschlagen
 11515-11536  _dashboard_adresse
 20384-20407  _db_maintenance_loop
  6628-6656   _db_vacuum_loop
 15528-15552  _detect_foreign_ad
  1553-1564   _diag_path_owner
 16793-16837  _director_finalize
 17755-17762  _director_for
 16742-16790  _director_mark
 21273-21276  _disc_state_get
 21279-21286  _disc_state_set
 20312-20321  _discord_bot_starten
 20275-20286  _discord_einladung_merken
 20324-20328  _discord_invite
 20289-20309  _discord_kontext
 21234-21270  _discord_live_thread
 16944-16956  _discord_notify
 20247-20272  _discord_ops_alert
 21132-21230  _discord_post_user
 20877-20883  _discord_stop
  6687-6764   _disk_alarm_loop
 23474-23523  _disk_autoclean
 23694-23707  _disk_guard_loop
 13315-13322  _drossel_hoeher
 13311-13312  _drossel_stufe
 13325-13333  _drossel_zuruecksetzen
 11692-11694  _dump_all_threads
 10246-10309  _enrich_proxies_with_geo
  2131-2192   _ensure_cookie_file_netscape
  8595-8598   _ensure_notify_topic
 10490-10527  _ensure_proxy_ready
  8549-8576   _ensure_topic
   717-719    _env_int
   722-724    _env_int_range
 16989-17002  _event_webhook
 12365-12378  _evolution_loop
  5812-5846   _extract_file_payload
  2264-2266   _extract_urls_from_streamurl_node
 19775-19782  _f2b_sudo_hint
 24183-24246  _fatal_vom_botteil
  4656-4666   _fehler_text
 10147-10165  _fetch_proxy_list
 17542-17570  _fetch_tiktok_room_id
   800-803    _ff_cmd
 13144-13149  _find_chromium
  3394-3396   _find_external_recorder
  2269-2271   _find_stream_urls
 12065-12090  _fire_webhooks
  7596-7605   _fork_safe
   901-914    _freeai_chat_sync_metered
 19821-19825  _geo_lookup_ips
  3660-3669   _get_ai_session
  7429-7469   _get_live_info
  2887-2894   _get_resolve_semaphore
  7878-8250   _handle_single_tracking
 23296-23298  _hb
 23301-23318  _hb_while
 12621-12623  _highlight_cfg
 12626-12655  _highlight_observe
 13152-13170  _htmlov_screenshot_cmd
 17248-17258  _httpx_proxy
 12098-12110  _in_quiet_hours
 24075-24086  _init_db_oder_abbruch
 24823-24854  _install_fast_eventloop
  9374-9428   _install_fast_json
 11697-11713  _install_faulthandler
 18488-18497  _intel_ensure_schema
 18535-18570  _intel_index_loop
 18509-18519  _intel_index_one
 18500-18506  _intel_semantic
  5181-5190   _is_authorized
  7779-7785   _is_dead
  2254-2256   _is_hevc
 19810-19812  _is_private_ip
  1771-1778   _is_process_running
  6400-6407   _is_quiet_hours
  1346-1355   _is_upload_window
  4521-4536   _iso
  9463-9476   _json_error_handler
  6622-6623   _kick_broadcaster_id
  6534-6576   _kick_follower_count
  6518-6521   _kick_slug
 11147-11154  _kick_user_token
 24063-24072  _kickmod_boot
  4111-4114   _kind_from_filename
 12127-12129  _latest_popularity
  1708-1717   _laufstand
 23657-23691  _laufstand_loop
 18151-18200  _live_react_loop
 17828-18140  _live_react_worker
 16392-16403  _live_transcript_push
 18142-18149  _live_users
 16840-16884  _living_title_loop
 20550-20622  _local_backup_scan
  9445-9459   _log_5xx
   790-797    _log_sicher
 13709-13721  _looks_like_codec_err
 13704-13706  _looks_like_source_expired
  7646-7676   _loop_fehler
 11717-11726  _loop_heartbeat
 23266-23293  _loop_lag_monitor
 11729-11797  _loop_watchdog_thread
 16272-16286  _loyalty_add
 16263-16269  _loyalty_get
 16289-16297  _loyalty_top
 12237-12239  _manual_donations_total
  4863-4882   _manual_status
  7787-7788   _mark_dead
 10766-10782  _marketing_loop
 21839-21857  _maybe_handle_command
 23793-23817  _maybe_hype_clip
 20927-20955  _meme_klassifizieren
  3989-4012   _migrate_columns
 22118-22129  _mod_is_exempt
 22132-22137  _mod_warn_first
 22140-22143  _mod_warn_text
 12405-12413  _modlog
  1046-1048   _multistream_targets
  3066-3102   _nachschlag_ytdlp
  7608-7609   _nc_create_subprocess_exec
  7612-7613   _nc_create_subprocess_shell
 11084-11101  _news_loop
 12432-12434  _normalize_ingest
  2486-2503   _note_check_duration
  8589-8592   _notify_topic_name
  3105-3125   _ohne_url_melden
 16418-16426  _oracle_memories
 16691-16725  _oracle_memorize
 16429-16442  _oracle_persona
 16411-16415  _oracle_recent_text
 12778-12779  _ov_atomic_write
 12769-12771  _ov_bar
 15431-15443  _ov_clip_text
 12774-12775  _ov_oneline
 19487-19516  _overlay_push
 13098-13141  _overlay_render_size
 12501-12505  _overlay_session_reset
 19452-19454  _overlay_src_ok
 15515-15525  _own_invites
 13093-13095  _parse_size
 19996-20076  _parse_ssh_attacks
  7031-7064   _pause_resume_cmd
  2013-2057   _persist_refreshed_cookies
  1916-1948   _pick_checked_pull_proxy
  9544-9557   _pin_auth_value
  9603-9604   _pin_clear_fail
  9583-9586   _pin_locked
  9589-9600   _pin_note_fail
  9560-9580   _pin_ok
 19296-19321  _piper_pick_model
 19381-19430  _piper_say
 12027-12062  _post_json_threaded
 13072-13090  _probe_video_size
  1799-1816   _proc_is_recorder
 10459-10487  _proxy_pool_refresh_loop
  1882-1913   _proxy_report_recording
 11682-11684  _prune_stall_dumps
 10836-11006  _public_stats
  2079-2085   _pull_proxy_still
 16960-16986  _push_notify
  9763-9765   _pwa_dir
 10216-10231  _quick_validate_proxy
 12093-12095  _quiet_hours_config
  9728-9761   _rate_guard
 16233-16239  _react_warn
  7516-7555   _reap_proc
  8823-8890   _rec_auto_abschalten
  8770-8820   _rec_frueh_getrennt
  8653-8715   _rec_kategorie_melden
  8718-8767   _rec_totstreak_fortschreiben
  2526-2548   _record_check_outcome
   785-787    _redact_stream_urls
 10386-10456  _refresh_proxy_pool
  2303-2394   _resolve_via_html
  2667-2864   _resolve_via_webcast_api_v2
  2927-3014   _resolve_via_ytdlp
 21448-21577  _resolve_youtube_ingest
  2280-2300   _resolver_stumm
 12484-12495  _restream_active_sources
 13421-13545  _restream_avatar_feeder_start
 13548-13557  _restream_avatar_feeder_stop
 17601-17719  _restream_chat_guardian
 12658-12730  _restream_chat_push
 12755-12764  _restream_chat_push_async
 13173-13282  _restream_html_overlay_start
 13285-13298  _restream_html_overlay_stop
 12443-12466  _restream_overlay_files
 18204-18236  _restream_platform_state
 18404-18439  _restream_resume_after_restart
 13605-13663  _restream_tts_enqueue_wav
 13034-13066  _restream_tts_feeder
 13031-13032  _restream_tts_fifo_path
 13560-13587  _restream_tts_start
 13589-13603  _restream_tts_stop
 18242-18401  _restream_verify_loop
 20515-20527  _retention_loop
 20509-20512  _retention_scan
  2624-2626   _room_is_abo
  5850-5967   _run_ai_call
 11820-11833  _run_async_from_flask
 19815-19818  _run_priv
 24811-24819  _run_selfcheck_and_exit
 20530-20541  _s3_client
  7814-7865   _safe_send
  4789-4805   _sample_net_throughput
  2578-2599   _schedule_next_check
 20463-20506  _scheduler_loop
  4015-4019   _schema_pk
 11837-11842  _scraper_session
 22146-22185  _screen_full
 11198-11235  _sec_headers
  2259-2261   _select_stream_from_data_section
 24536-24808  _selfcheck
  8601-8635   _send_live_notice
  1369-1373   _should_defer_upload
 21001-21036  _shrink_for_discord
  9768-9780   _sicheres_ziel
 20343-20381  _sicherheits_erinnerung_loop
 23714-23731  _sign_health_check
 23734-23753  _sign_health_loop
  4539-4564   _sitzung_bestimmen
  7625-7636   _spawn
 25236-25266  _spawn_from_flask
 17260-17539  _start_chat_listener
 11800-11817  _start_loop_watchdog
 11033-11079  _stats_loop
 11012-11015  _stats_output_path
 11018-11030  _stats_write
 19333-19347  _stimme_saubern
 19354-19378  _stimme_schon_gesagt
  8329-8345   _storage_cleanup_loop
 23773-23780  _story_for
  3419-3425   _stream_url_expiry
  3427-3432   _stream_url_ttl
 15478-15485  _streamer_persona_get
 20647-20769  _system_backup
 20778-20808  _system_backup_loop
 11642-11660  _task_auf_bot_schleife
 22959-22975  _telegram_befehlsmenue
  7679-7725   _telegram_polling_fehler
 10168-10207  _test_proxy
 10714-10730  _testpush_resolve_live
  7790-7811   _tg_sprache_setzen
  8508-8518   _tg_topics_load_into_mem
  8505-8506   _tg_topics_path
  8520-8527   _tg_topics_save
  9518-9526   _token_ok
  8530-8534   _topic_forget
 12113-12124  _tracking_max_duration
  4319-4333   _tracking_remove_cleanup
  4350-4362   _tracking_resume_cleanup
  1611-1634   _try_attach_file_handler
 19323-19331  _tts_cleanup
 10690-10694  _tunnel_effective
 23526-23546  _tunnel_lage
 23602-23654  _tunnel_wacht_loop
 18819-18872  _twitch_channel_status
 22188-22333  _twitch_chat_loop
 21292-21305  _twitch_clip_versuchen
 22002-22105  _twitch_eventsub_loop
  1392-1405   _upload_queue_add
  1416-1418   _upload_queue_count
  1375-1384   _upload_queue_load
  1365-1367   _upload_queue_path
  1407-1414   _upload_queue_remove
  1386-1390   _upload_queue_save
  1420-1461   _upload_window_loop
  7489-7496   _uptime_s
 12420-12429  _url_host
  3128-3222   _url_nachschlag
   861-865    _usage_record_claude
 23887-23909  _v37_pause_source
 23851-23861  _v37_restream_restart
 23864-23884  _v37_unpause_source
  7728-7772   _verbindung_verloren
  6579-6610   _viewer_sample_loop
  9607-9610   _wants_html
  7499-7513   _warn_empty_env
 23339-23460  _watchdog_loop
 21723-21731  _wchat_thank_ok
 17028-17058  _whisper_get_model
  7586-7593   _whisper_native_section
 16220-16226  _whisper_pool
 17152-17184  _whisper_segments
 17060-17076  _whisper_stumm
 17079-17149  _whisper_transcribe
 12826-12988  _write_restream_overlay
 12788-12823  _write_restream_overlay_async
 22357-22453  _youtube_api_chat_loop
 18875-18978  _youtube_api_status
 18981-19048  _youtube_channel_status
 22456-22617  _youtube_chat_loop
 21308-21333  _youtube_clip_versuchen
 21583-21596  _youtube_restream_autoconfig
 21599-21623  _youtube_restream_autoconfig_inner
 21690-21718  _youtube_send
 19116-19157  _youtube_set_channel
 21626-21660  _yt_access_token
 21663-21678  _yt_live_chat_id
 21686-21687  _yt_sendrate_cfg
 22336-22351  _yt_timeout
  2911-2912   _ytdlp_detect_available
  2914-2925   _ytdlp_note_result
 11687-11689  _zombie_child_count
  7365-7389   about
  4230-4234   add_ai_log_entry
  4147-4150   add_archive_entry
  4827-4829   add_archive_rule
  4567-4638   add_recording
  4294-4311   add_tracking
  5970-6003   ai
  3812-3893   ai_chat
  3927-3937   ai_history_append
  3939-3944   ai_history_clear
  3916-3925   ai_history_load
  3901-3914   ai_rate_limit_check
  6032-6040   aireset
 16559-16578  azrael_chat
 22622-22744  brain_cmd
  3435-3440   build_recording_cmd
  4314-4317   bulk_add_trackings
  6833-6892   bulkadd
  8348-8488   check_all_trackings
  4366-4378   claim_live_transition
 15555-16152  class KickModerator
 13724-15318  class RestreamManager
 10573-10615  classify_proxy_anonymity
  6078-6276   cleanup
  5117-5123   cleanup_old_recordings
  4512-4519   clear_recording
 21336-21405  clip_moment
  4779-4782   compute_storage_forecast
  6955-7028   cookies_cmd
  4285-4291   count_trackings_for_chat
  4217-4228   decide_preferred_recorder
  4157-4160   delete_archive_entry
  4831-4833   delete_archive_rule
  5507-5654   diag
 22856-22917  einnahmen_cmd
  4773-4776   find_recordings_by_fingerprint
  4178-4194   finish_recording_attempt
  4338-4340   get_all_active_trackings
  4245-4247   get_all_checks
  4640-4643   get_all_recordings
  4722-4724   get_all_tags_with_counts
  4750-4753   get_annotations_for_recording
  4152-4155   get_archive_entry
  4743-4746   get_bookmarked_recordings
  2119-2124   get_cookie_health
  4710-4716   get_event_log
  4201-4215   get_last_recording_attempt
  3225-3356   get_live_status
  5056-5059   get_manual_recordings
  4758-4761   get_or_compute_inspect_sync
  5158-5161   get_outcome_breakdown
  4729-4732   get_priority_poll_interval
  4196-4199   get_recent_recording_attempts
  4645-4648   get_recording_by_id
  4736-4739   get_recording_note
  3606-3629   get_redis
  4274-4277   get_stats
  5111-5115   get_storage_stats
  4851-4853   get_tiktok_status_distribution
  4380-4389   get_tracking_state
  4335-4336   get_trackings_for_group
  5072-5075   get_trash_recordings
  8893-9353   handle_recording_finished
 22951-22956  hilfe_cmd
  4042-4102   init_db
  4823-4825   list_archive_rules
  5311-5349   live
  7868-7876   live_check_worker
  3684-3723   llm_chat
  3746-3776   llm_chat_sync
  3731-3743   llm_list_models
  4669-4702   log_event
  1733-1766   log_recording_failure
  7178-7227   logs_cmd
 24249-24526  main
  6006-6029   on_ai_media
  7304-7330   on_ai_reply
  7333-7362   on_azrael_mention
  7394-7424   on_callback
 16584-16688  oracle_handle
  7067-7070   pause_tracking
  5171-5176   profile_keyboard
  7129-7175   quota
  8252-8326   reaper_loop
  4847-4849   record_tiktok_status
  6045-6075   recstatus
  3631-3639   redis_get_json
  3642-3648   redis_set_json
 22978-22988  report_cmd
 10618-10620  report_proxy_result
  2397-2439   resolve_tiktok_live_stream
  5067-5070   restore_recording
  7073-7076   resume_tracking
  4836-4841   run_archive_rules
 22991-23246  run_bot
 11539-11633  run_flask
  4811-4814   sample_bandwidth_for_active
  4237-4243   save_tiktok_check
  4504-4510   set_recording_file
  4343-4347   set_tracking_paused
  5062-5065   soft_delete_recording
  8641-8651   split_and_send_video
  5224-5266   start
  4162-4176   start_recording_attempt
  6279-6317   stats
  5001-5054   stop_manual_recording
  7079-7126   stoprec
  6503-6511   summary_cmd
  7230-7301   sysres
  5656-5800   teststream
  5268-5309   tiktok
  6895-6952   topusers
  5386-5443   track
  5351-5383   track_exact
  5457-5505   tracklist
  4885-4999   trigger_manual_recording
  4465-4502   try_acquire_recording_lock
  5078-5080   universal_search
 22920-22948  unpause_cmd
  5445-5455   untrack
 22747-22853  update_cmd
  4768-4771   update_recording_fingerprint
```

## nc/ — öffentliche Symbole

```
__init__.py            —
abo.py                 room_is_abo
admod.py               build_allowlist
aidb.py                add_log_entry, conv_messages
archive.py             add_archive_entry, class BestandUnbekannt, compute_recording_fingerprint, configure, delete_archive_entry, evaluate_archive_rule, finde_ohne_eintrag, get_archive_entries_paged, get_archive_entry, run_archive_file_check, uebernehmen
archivename.py         open_unique
archiverules.py        add_archive_rule, delete_archive_rule, list_archive_rules, run_archive_rules
audio_cue.py           cue_pcm, duck_ratio, mix_chain, silence_pcm, tone_pcm
audiocue.py            config, configure
audiotap.py            diagnose, melden, warum_kein_tap
aufnahmefolge.py       aufnahme_geglueckt, daten_geflossen, melden_erlaubt, nach_403, nach_frueher_trennung, nach_totem_versuch, sitzung_zuende, sperre_rest
aufnahmekategorie.py   kategorisiere
aufnahmesitzung.py     abdeckung, concat_cmd, concat_liste, gehoert_dazu, luecken, sekunden, sitzung_id, zieldatei
auslieferung.py        schreibe, stand, text
avatarloop.py          blinzeln, ruhe_seit, schleife, zustand
azraelstate.py         configure, flag, haken, personas_load, personas_path, personas_save
backupcfg.py           aktiv, fehlgrund, lokal, lokal_dir, recordings_retain_days, retention_days, s3, s3_bucket, s3_endpoint, s3_konfiguriert, s3_region, s3_zugang, sys_backup, sys_hour, sys_keep, sys_max_file_mb
badwords.py            banned_path, configure, fetch_ldnoobw_de, learned_path, load_banned, load_learned, save_banned, save_learned
bandbreite.py          messen
befehle.py             beschreibung, discord_nativ, discord_ueber_tg, fuer, hilfe_text, pruefen, telegram_handler
binresolve.py          resolve
botctx.py              class BotKontext
brainstate.py          history_for, record, stall, stream_recent
cfgnorm.py             normalize_audio, normalize_cohost, normalize_gate, normalize_highlights, normalize_quiet_hours, normalize_sendrate
cfgstore.py            get, set_, upsert
channels.py            configure_chat, restream_active, yt_sendrate_cfg
chatfolge.py           entscheide
chatstats.py           summarize
claude.py              api_key, build_payload, chat_sync, fehlertext, is_retired, model, model_raw, parse_response, parse_usage, probe, resolve_model, test_key
cohost.py              config, decide, default_config, new_state, prompt_seed, snapshot
community.py           anzeigename, configure, darf_pingen, highlight_post, highlight_share_enabled, live_ping, live_ping_enabled, note_chatter, returning_enabled, rollen_id, seen_stats
confdrift.py           config_drift, extract_defaults, log_watchlist_drift
convmap.py             messages
cookiebezug.py         anstossen, configure, faellig, gast_hilft, holen, info, intervall_s, naechster_lauf
cookieholen.py         aktualisiere, aus_browser, configure, hole_gastcookies, schreibe, zusammenfuehren
cookies.py             configure, gesundheit, lade_jar, load_dict
creatoragg.py          summarize
crowdsec.py            base_url, decisions_url, explain_status, headers, parse_decisions
crypto.py              addresses, erwartete_namen, fehlende_namen, snapshot
ctx.py                 class Ctx, configure, get, is_configured
dashauth.py            erlaubt_offen, geschuetzt, host, lage, nur_lokal, offen_im_netz, zurueckgefallen
dbexport.py            db_export_sql, db_import_sql, export_summary, parse_header
dbrestore.py           archive, dump_aus_archiv, einsetzen, einspielen, vorbereiten
dbwrap.py              class DatenbankUnlesbar, configure_db, datei_diagnose, db_async, db_conn, get_pool, set_pool
ddlsafe.py             ddl, ist_schon_da
defensecfg.py          bouncer_gesetzt, bouncer_key, geo_fehler, geo_fehler_setzen, lapi_host, lapi_port, lapi_url, server_lat, server_lon
director.py            class LiveDirector, configure
discordlimits.py       aktuell_label, aktuell_mb, configure, describe, effective_upload_mb, gate_mb, guild_filesize_bytes, guild_limit_mb
discordrang.py         rang_fuer_level, slug, xp_fuer_level, xp_zu_level
discordstate.py        invite, state_get
donations.py           configure, fmt_eur, parse_number, source_allowed, to_eur, unknown_count
donationsdb.py         manual_rows, manual_total, parse_eur
envnum.py              clamp_float, clamp_int, env_float, env_int, env_int_range
eventlog.py            leeren, schreibe, stand
eventquery.py          build_query
evolution.py           analyze, build_dir, conf, configure, cycle, engineering_note, next_version, write_build
fehlertext.py          nach_aussen, saeubern
ffbuild.py             ff_cmd
ffdiag.py              clip_caption_escape, ffprobe_duration, redact_cmd_for_log
ffmpeg_filters.py      avatar_kette, chat_umbruch_w, chat_zeilen, drawtext_chain, studio_chain, studio_masse
ffver.py               parse_version
filepayload.py         classify_downloaded, size_reject
flapguard.py           class FlapConfig, class FlapUrteil, class FlapWatch
fmt.py                 fmt_duration, fmt_size_mb, pre_table, utc_clock
freeai.py              alive_sync, bases_status, chat, chat_stream, chat_sync, configure, diagnose, dienstmeldung, katalog_kennt, last_errors, list_models_sync, stream_haeppchen, stream_rest
geocache.py            get, groesse, leeren, put
geoip.py               ist_privat, lookup
highlights.py          check, new_state, observe, score, zustand
i18n.py                aktuelle_sprache, aus_accept_language, configure, katalog, normalisieren, sprache_setzen, standard, t
inspectcache.py        parse_row, serialize
journalperm.py         may_read
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, token_exchange_payload, token_refresh_payload
kickapi.py             app_token, broadcaster_id, channel_info, configure, oauth_exchange, search_category, send_message, slug, timeout_user, update_channel, user_token
kiwahl.py              backend, lokal_stand, lokal_zuerst, normal, provider
lastvorsorge.py        freie_kerne, jung, startstufe
laufstand.py           befehl, veraltet, vergleich
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
livecache.py           aufraeumen, frisch, holen, setzen
livefolge.py           braucht_url_nachschlag, hat_stream_url, live_gesehen, offline_bestaetigt, poll_abstand, ruhezeit
logfilters.py          configure_logfilters
loginpage.py           login_page
logsafe.py             fuer_log, redact_cookie_zeilen, redact_pull_urls, redact_stream_urls, url_ohne_zugang
logschleuse.py         class Schleuse, entkoppeln, stoppen, verloren, wartend, zuruecksetzen
loyalty.py             award_chat, award_return, configure, enabled, leaderboard, rank_for, status
marketing.py           ai_flavor, class MarketingConfig, class MarketingState, compose, config, configure, default_targets, enabled, has_content, next_due_ts, post_discord, post_telegram, publish, should_post, state, state_save, variants
meldetakt.py           melden, zuruecksetzen, zusatz
memeklip.py            class Fenster, frage, lies_urteil, soll_clippen
modheuristics.py       caps_ratio, count_links, count_mentions, escalation_minutes, escalation_step, flood_reason, is_caps_spam, is_exempt, kick_roles, prune_history, prune_infractions, resolve_exempt, stateless_reason, twitch_roles
modki.py               frage, lies_klassifikation, lies_schimpfwoerter
modstats.py            ist_moderation, plattform, quellen, verdichte, zaehlt
netstat.py             sum_bytes, throughput_kbps
news.py                absaetze, azrael_creator_take, build_items, class NewsConfig, class NewsState, collect_facts, config, configure, creator_activity, creator_dossier_generate, creator_facts_line, enabled, generate, item_id, merge, output_path, phrase, phrase_impl, read_items, render_json, should_generate, state, state_save, write_items
notes.py               add_annotation, delete_annotation, set_recording_note, set_tracking_notes, toggle_bookmark
oauthpage.py           kick, twitch
oauthredirect.py       configure, public_base_url, redirect_env, redirect_public, redirect_source, redirect_uri
outcomes.py            get_outcome_breakdown
overlaytext.py         configure, latest_popularity, ov_atomic_write, ov_bar, ov_oneline, overlay_src_ok
persona.py             —
piper_voices.py        available, bin_pfad, configure, data_dir, list_voices, resolve, resolve_model_path, roots, voice_dirs, voice_roots
preflight.py           configure
procdiag.py            dump_all_threads, prune_stall_dumps, zombie_child_count
proxyutil.py           class ProxyHealth, configure_proxy_select, configure_proxyhealth, configure_router, get_random_proxy, proxy_pool, record_proxy, tunnel_effective, tunnel_state
qrsvg.py               qr_svg
reccmd.py              build_recording_cmd, configure
recdb.py               configure, find_recordings_by_fingerprint, get_all_checks, get_all_recordings, get_annotations_for_recording, get_bookmarked_recordings, get_manual_recordings, get_or_compute_inspect_sync, get_recent_recording_attempts, get_recording_by_id, get_recording_note, get_trash_recordings, restore_recording, soft_delete_recording, update_recording_fingerprint
recdiag.py             class RateConfig, class RateSpur, disconnect_analysis, url_refresh_stats
replygate.py           allow, default_config
resolvergrund.py       http_grund, quelle_lage, quelle_laut, text
restream_guard.py      class GuardConfig, class RestreamGuard, class RestreamState, class TargetState, classify
restream_stability.py  budget_after_run, budget_exhausted, class ReconnectPolicy, class StallVerdict, expired_delay, expired_is_spinning, expired_streak, is_codec_failure, looks_like_network_failure, reconnect_delay, stall_verdict
restream_targets.py    active_targets, build_output_args, configure, multistream_targets, single_output_args
restream_testpush.py   build_cmd, class GuardDecision, class ResolvedTarget, class TestPushConfig, classify_result, fingerprint, guard, resolve_target
restream_util.py       betroffene_ziele, fenstergroesse, http_url, looks_like_source_expired, normalize_ingest, slot_belegt, url_host
restreamcfg.py         active_platforms, aktiv, bereite_ziele, chat_src_ok, discord_invite, enabled, ingest, key_gesetzt, kick_channel_url, overlay, stall_timeout, verify, verify_karenz, verify_misses, verify_takt, yt_oauth_configured, ziel
restreamcmd.py         build, configure, drossel_avatar_aus, drossel_bitrate, drossel_canvas, drossel_fps, drossel_preset, drossel_zusatz, schriftart
restreamgesundheit.py  blind_markieren, frische_tee_fehler, marke_setzen
restreamstate.py       guard, haken, laufende, layout_mode, mgr
restrend.py            rising_trend
retention.py           scan
revenue.py             is_revenue_platform, normalisieren, sql_in
schema.py              create_schema
schemastand.py         lege_an, lies, pruefe, schreibe, streng
scoring.py             build_report, compute_quality_score
scraper.py             class TikTokScraper, configure_scraper
sendrate.py            allow, default_config, new_state, snapshot
shield.py              —
sicherpfad.py          pruefe_unter, sicher_join, sicherer_name, unter
sqlguard.py            check_readonly, normalize, with_limit
sqlutil.py             —
stats.py               configure_stats, get_activity_pulse, get_lives_heatmap, get_per_user_stats, get_recordings_heatmap, get_stats, get_tiktok_status_distribution, invalidate_stats_cache
storage.py             cleanup, forecast, stats
story.py               class StoryMemory, configure
streamsel.py           extract_urls_from_streamurl_node, find_stream_urls, is_hevc, select_stream_from_data_section
suche.py               universal_search
sysload.py             classify_load, parse_meminfo, parse_ps
sysrun.py              run_priv
systemprobe.py         active_recorder, ai_alive, ai_calls_total, cache_leeren, cached_probe, configure, cpu_load_snapshot, disk_pct, recorder_pref, recordings_dir, redis_alive, redis_url, redis_version
telegramfehler.py      dauer_text, grund, ist_fehler, text, zuruecksetzen
textmore.py            configure_banned_cap, split_for_telegram
textutil.py            clean_username, fmt_number, is_valid_tiktok_username, safe, short
tiktokcheck.py         account_exists, configure
tiktokheaders.py       configure
tonspur.py             class Fehlschlag, hat_ton, hat_tonspur, ist_tonlos_fehler, nachruest_cmd, pruef_cmd, pruefen, sichern, stille_eingabe
trackingdb.py          add_tracking_tag, bulk_add_trackings, ci_key, claim_transition, configure, get_all_active_trackings, get_all_tags_with_counts, get_priority_poll_interval, get_state, get_tags_for_tracking, get_tracking_priority, get_trackings_for_group, remove_tracking, remove_tracking_tag, resolve_tracked_user, set_tracking_paused, set_tracking_priority
tunnelwacht.py         lage, meldung, probe, probe_cmd
twitchoauth.py         access_token, authorize_url, configure, create_clip, exchange_code, forget, login_name, search_category, status, timeout_user, update_channel
updater.py             build_plan, check, class Plan, class UpdaterConfig, configure, describe, download_zip, is_protected, job_state, list_backups, local_head, local_state, normalize, remote_head, repo_url, rollback, run_update, settings, sha256_bytes, sha256_file, short_sha, start_update, strip_archive_root, zip_url
usage.py               configure, estimate_tokens, flush, record, snapshot
util.py                datei_in
version.py             build_stamp, changelog, current, latest, summary_line
videoteil.py           configure, dauer, ist_kaputter_container, kopier_teilen, neu_kodieren, platz_reicht, reparieren, wegwerfen, zeitstempel_richten, zu_gross
webserver.py           bindung, ist_loopback, schema, threads, tls_lage, waehle
whispercfg.py          geladen, name, verfuegbar, waehle
youtube_api.py         active_broadcast_params, ban_payload, is_self, list_params, merge_video_snippet, parse_broadcast_id, parse_error, parse_messages, parse_video_snippet, video_list_params, video_update_body
ytdlpurl.py            urls_aus_json
ytoauth.py             access_token, authorize_url, configure, exchange_code, forget, invalidate_access, revoke, set_channel, status, upload_clip
```

## brain/ — öffentliche Symbole

```
__init__.py            class Brain, get_brain
agents.py              class Agent, class AgentManager, class AnalyticsAgent, class DiskAgent, class HealthAgent, class LearningAgent, class ProxyHealthAgent, class RecordingAgent, class RecoveryAgent, class RestreamSentinelAgent, class ScoutAgent, class SentinelAgent, class SwapAgent, class ToxicityAgent, class UptimeAgent
knowledge.py           class KnowledgeGraph
llm.py                 class BudgetExhausted, class LLMRuntime
memory.py              class Memory
report.py              weekly
router.py              class Task, class TaskRouter, class Unhandled
rules.py               class Rule, class RulesEngine
scheduler.py           class Scheduler
semantic.py            class SemanticMemory
state.py               class Entity, class StateMachine
test_bughunt.py        db_conn, main
test_m1.py             main
test_m3.py             main
test_m4.py             main
test_m5.py             main
test_m6.py             class LlamaCppMock, main
test_m7.py             db_conn, main
```
